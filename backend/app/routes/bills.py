# routes/bills.py
# POST /upload-bill  –  accept file, run OCR, return extracted data

import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.ocr_service import process_bill
from app.models.schemas import Expense
from app.utils import store

router = APIRouter()

ALLOWED_TYPES = {
    "image/jpeg", "image/png", "image/jpg",
    "application/pdf",
}
MAX_SIZE_MB = 10


@router.post("/upload-bill")
async def upload_bill(file: UploadFile = File(...)):
    """
    Accept a JPG / PNG / PDF bill, run OCR, persist as an Expense entry,
    and return the extracted + stored data for immediate display.
    """
    # ── Validate content type ─────────────────────────────────────────────────
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{file.content_type}'. "
                   f"Please upload JPG, PNG, or PDF.",
        )

    # ── Read bytes (process in memory, never persist to disk) ─────────────────
    file_bytes = await file.read()
    if len(file_bytes) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds {MAX_SIZE_MB} MB limit.",
        )

    # ── OCR + field extraction ────────────────────────────────────────────────
    extracted = process_bill(file_bytes, file.filename or "bill")

    # ── Build Expense record and save to in-memory store ─────────────────────
    expense_id = str(uuid.uuid4())
    expense = Expense(
        id=expense_id,
        bill_name=file.filename or f"bill_{expense_id[:8]}",
        vendor=extracted["vendor"],
        category=extracted["suggested_category"],
        expense_type="Personal",          # default; user can change
        amount=extracted["total_amount"],
        gst=extracted["gst_amount"],
        date=extracted["bill_date"],
    )
    store.expenses[expense_id] = expense

    return {
        "id": expense_id,
        "bill_name": expense.bill_name,
        "vendor": expense.vendor,
        "category": expense.category,
        "expense_type": expense.expense_type,
        "amount": expense.amount,
        "gst": expense.gst,
        "date": expense.date,
        "raw_text": extracted["raw_text"],
        "message": "Bill processed successfully.",
    }
