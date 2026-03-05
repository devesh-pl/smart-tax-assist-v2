# services/ocr_service.py
# OCR extraction and field-parsing logic for bill images and PDFs

import re
import io
import logging
from typing import Optional

from PIL import Image

logger = logging.getLogger(__name__)

# ── Optional heavy imports ────────────────────────────────────────────────────
try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    logger.warning("pytesseract not available – OCR disabled")

try:
    from pdf2image import convert_from_bytes
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logger.warning("pdf2image not available – PDF OCR disabled")


# ── Category keyword map ──────────────────────────────────────────────────────
CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "Food": ["restaurant", "cafe", "pizza", "burger", "grocery", "supermarket",
             "bakery", "coffee", "diner", "food", "meal", "lunch", "dinner",
             "chicken", "biryani", "roti", "dal", "tandoori", "dhaba"],
    "Fuel": ["fuel", "petrol", "gasoline", "diesel", "bp", "shell", "mobil",
             "chevron", "esso", "filling station", "pump"],
    "Gas": ["gas", "natural gas", "propane", "utility gas", "enbridge"],
    "Education": ["school", "university", "college", "tuition", "course",
                  "textbook", "education", "training", "workshop", "seminar"],
    "Travel": ["airline", "hotel", "motel", "airbnb", "uber", "lyft", "taxi",
               "transit", "bus", "train", "flight", "booking", "expedia"],
    "Office Supplies": ["staples", "office depot", "officeworks", "printer",
                        "stationery", "supplies", "paper", "ink", "toner"],
    "Utilities": ["hydro", "electricity", "water", "internet", "phone",
                  "telecom", "rogers", "bell", "at&t", "verizon", "utility"],
}


# ── OCR helpers ───────────────────────────────────────────────────────────────

def extract_text_from_image(image_bytes: bytes) -> str:
    if not OCR_AVAILABLE:
        return ""
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        return pytesseract.image_to_string(image, config="--psm 6")
    except Exception as exc:
        logger.error("OCR image extraction failed: %s", exc)
        return ""


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    if not PDF_AVAILABLE:
        return ""
    try:
        pages = convert_from_bytes(pdf_bytes, dpi=200)
        texts = [pytesseract.image_to_string(p, config="--psm 6") for p in pages] if OCR_AVAILABLE else []
        return "\n".join(texts)
    except Exception as exc:
        logger.error("OCR PDF extraction failed: %s", exc)
        return ""


# ── Amount extraction ─────────────────────────────────────────────────────────

# Matches the RIGHTMOST monetary value on a line (anchored to end-of-line).
# Handles: 1,139.00 / 25.89 / 1035 / ₹309.75
_MONEY_RE = re.compile(
    r"(?:[\$\u00a3\u20ac\u20b9]?\s*)"    # optional currency symbol
    r"(\d{1,7}(?:,\d{2,3})*"             # integer part with optional comma groups
    r"(?:\.\d{1,2})?)"                   # optional decimal
    r"\s*$",                             # MUST be at end of line
)

# Lines that are ONLY a small bare integer are qty/count rows — skip them.
_QTY_ONLY_RE = re.compile(r"^\s*\d{1,3}\s*$")


def _extract_rightmost_amount(line: str) -> Optional[float]:
    """
    Return the rightmost plausible monetary value from a line, or None.

    Rejects:
    - Lines whose entire content is a bare small integer (e.g. '6' = Total Qty).
    - Values < 10 that carry no currency symbol (almost certainly a qty/rate col).
    """
    stripped = line.strip()
    if _QTY_ONLY_RE.match(stripped):
        return None

    m = _MONEY_RE.search(stripped)
    if not m:
        return None

    try:
        value = float(m.group(1).replace(",", ""))
    except ValueError:
        return None

    has_symbol = bool(re.search(r"[\$\u00a3\u20ac\u20b9]", stripped))
    if value < 10 and not has_symbol:
        return None   # looks like a quantity (e.g. 1, 2, 6)

    return value


# ── Field parsers ─────────────────────────────────────────────────────────────

def parse_vendor(text: str) -> str:
    """First mostly-alphabetic, non-digit-starting line is the vendor name."""
    for line in text.splitlines():
        line = line.strip()
        if len(line) < 3 or re.match(r"^\d", line):
            continue
        alpha_ratio = sum(c.isalpha() for c in line) / len(line)
        if alpha_ratio >= 0.4:
            return line[:80]
    return "Unknown Vendor"


def parse_date(text: str) -> Optional[str]:
    """
    Extract a date from OCR text.  Prefers lines containing the word 'date'.
    Handles: 20-May-18, 20/05/2018, 2018-05-20, May 20 2018, etc.
    """
    patterns = [
        r"\b(\d{1,2}[-/]\w{3,9}[-/]\d{2,4})\b",   # 20-May-18  ← this bill
        r"\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\b",
        r"\b(\d{4}[-/]\d{1,2}[-/]\d{1,2})\b",
        r"\b(\w{3,9}\s+\d{1,2},?\s+\d{4})\b",
        r"\b(\d{1,2}\s+\w{3,9}\s+\d{4})\b",
    ]
    lines = text.splitlines()
    date_lines = [l for l in lines if re.search(r"\bdate\b", l, re.IGNORECASE)]
    for line in date_lines + lines:
        for pat in patterns:
            m = re.search(pat, line, re.IGNORECASE)
            if m:
                return m.group(1)
    return None


def parse_total(text: str) -> float:
    """
    Extract the grand total / final payable amount.

    - Matches lines with 'total' (or synonyms) but EXCLUDES sub-total, qty, tax lines.
    - Returns the LAST match (the final 'Total: 1,139.00' line wins).
    - Reads the RIGHTMOST number on each candidate line.
    """
    TOTAL_RE = re.compile(
        r"\b(grand\s+total|amount\s+due|amount\s+payable|balance\s+due"
        r"|net\s+payable|total\s+amount|total)\b",
        re.IGNORECASE,
    )
    # Exclude lines that talk about tax components or sub-totals or quantities
    EXCLUDE_RE = re.compile(
        r"\b(sub\s*total|total\s+qty|total\s+quantity"
        r"|cgst|sgst|igst|utgst|vat|hst"
        r"|s\.?\s*tax|service\s+tax|sales\s+tax|gst)\b",
        re.IGNORECASE,
    )

    candidates: list[float] = []
    for line in text.splitlines():
        if TOTAL_RE.search(line) and not EXCLUDE_RE.search(line):
            amt = _extract_rightmost_amount(line)
            if amt is not None:
                candidates.append(amt)

    return candidates[-1] if candidates else 0.0


def parse_gst(text: str) -> float:
    """
    Sum ALL GST component lines: CGST, SGST, IGST, S.Tax, VAT, etc.

    Indian bills split GST into CGST + SGST — this function adds them together.
    e.g. CGST@2.5 → 25.89  +  SGST@2.5 → 25.89  =  51.78  (≈ S.Tax 51.75)

    Also catches a single 'S.Tax' or 'GST' summary line if present.
    De-duplication: if both component lines (CGST+SGST) AND a summary S.Tax
    line exist, we prefer whichever is larger / more granular.
    """
    GST_LINE_RE = re.compile(
        r"\b(cgst|sgst|igst|utgst|gst|hst|vat"
        r"|s\.?\s*tax|service\s+tax|sales\s+tax"
        r"|goods\s+and\s+services)\b",
        re.IGNORECASE,
    )
    # Skip bare rate-header lines like 'CGST@2.5' that trail off with no amount
    RATE_ONLY_RE = re.compile(r"@\s*\d+\.?\d*\s*%?\s*$")

    component_total = 0.0   # sum of CGST + SGST + IGST lines
    summary_total   = 0.0   # a single 'S.Tax / GST' summary line
    component_count = 0

    for line in text.splitlines():
        if not GST_LINE_RE.search(line):
            continue
        if RATE_ONLY_RE.search(line.strip()):
            continue

        amt = _extract_rightmost_amount(line)
        if amt is None:
            continue

        lower = line.lower()
        if re.search(r"\b(cgst|sgst|igst|utgst)\b", lower):
            component_total += amt
            component_count += 1
            logger.debug("GST component: %r → %.2f", line.strip(), amt)
        elif re.search(r"\b(s\.?\s*tax|service\s+tax|sales\s+tax|gst|vat|hst)\b", lower):
            # Could be a summary line; keep the larger one
            summary_total = max(summary_total, amt)
            logger.debug("GST summary:   %r → %.2f", line.strip(), amt)

    # Prefer component sum if we found at least two components (CGST + SGST);
    # otherwise fall back to the summary line.
    if component_count >= 2:
        result = component_total
    elif component_count == 1 and summary_total > 0:
        result = max(component_total, summary_total)
    else:
        result = summary_total or component_total

    return round(result, 2)


def suggest_category(text: str) -> str:
    """Auto-suggest a category by keyword matching."""
    lower = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in lower for kw in keywords):
            return category
    return "Other"


# ── Main entry point ─────────────────────────────────────────────────────────

def process_bill(file_bytes: bytes, filename: str) -> dict:
    """
    Extract all bill fields from raw bytes.
    Returns vendor, bill_date, total_amount, gst_amount, raw_text,
    and a suggested category.
    """
    ext = filename.lower().rsplit(".", 1)[-1]
    raw_text = (
        extract_text_from_pdf(file_bytes) if ext == "pdf"
        else extract_text_from_image(file_bytes)
    )
    if not raw_text.strip():
        raw_text = ""

    total = parse_total(raw_text)
    gst   = parse_gst(raw_text)

    # Sanity guard: GST must be less than total
    if total > 0 and gst >= total:
        logger.warning("GST (%.2f) >= total (%.2f); resetting GST to 0", gst, total)
        gst = 0.0

    return {
        "vendor":             parse_vendor(raw_text) if raw_text else "Unknown Vendor",
        "bill_date":          parse_date(raw_text),
        "total_amount":       total,
        "gst_amount":         gst,
        "raw_text":           raw_text,
        "suggested_category": suggest_category(raw_text),
    }