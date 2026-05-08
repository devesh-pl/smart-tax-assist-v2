# routes/bills.py
# POST /upload-bill  –  accept file, run OCR, return extracted data

from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from bson.objectid import ObjectId

from app.services.ocr_service import process_bill
from app.utils.db import get_expenses_collection
from app.utils.auth_dependency import get_current_user

router = APIRouter()

ALLOWED_TYPES = {
    "image/jpeg", "image/png", "image/jpg",
    "application/pdf",
}
MAX_SIZE_MB = 10


@router.post("/upload-bill")
async def upload_bill(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
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

    # ── Build Expense document and save to MongoDB ───────────────────────────
    expenses_col = get_expenses_collection()
    now = datetime.utcnow()
    
    expense_doc = {
        "user_id": ObjectId(current_user["_id"]),
        "bill_name": file.filename or "bill",
        "vendor": extracted["vendor"],
        "category": extracted["suggested_category"],
        "expense_type": "Personal",          # default; user can change
        "amount": extracted["total_amount"],
        "gst": extracted["gst_amount"],
        "date": extracted["bill_date"],
        "created_at": now,
        "updated_at": now,
    }
    
    result = expenses_col.insert_one(expense_doc)
    expense_id = str(result.inserted_id)

    return {
        "id": expense_id,
        "bill_name": expense_doc["bill_name"],
        "vendor": expense_doc["vendor"],
        "category": expense_doc["category"],
        "expense_type": expense_doc["expense_type"],
        "amount": expense_doc["amount"],
        "gst": expense_doc["gst"],
        "date": expense_doc["date"],
        "raw_text": extracted["raw_text"],
        "message": "Bill processed successfully.",
    }
