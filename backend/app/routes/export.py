from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.responses import StreamingResponse
from bson.objectid import ObjectId
import io

from app.services.auth_service import decode_token, get_user_by_id
from app.utils.db import get_expenses_collection
from app.utils.auth_dependency import get_current_user

router = APIRouter()


@router.get("/export-excel")
async def export_excel(token: str = Query(...)):
    """Generate and stream an Excel file of current user's expenses."""
    # Verify token manually since we're getting it from query parameter
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Get user from payload
    user = get_user_by_id(payload.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    expenses_col = get_expenses_collection()
    
    # Get all expenses for current user
    expenses_cursor = expenses_col.find(
        {"user_id": ObjectId(user["_id"])}
    )
    
    # Convert to list of dicts for excel service
    expenses = []
    for doc in expenses_cursor:
        doc_dict = {
            "id": str(doc["_id"]),
            "bill_name": doc.get("bill_name", ""),
            "vendor": doc.get("vendor", ""),
            "category": doc.get("category", ""),
            "expense_type": doc.get("expense_type", ""),
            "amount": doc.get("amount", 0),
            "gst": doc.get("gst", 0),
            "date": doc.get("date", ""),
        }
        expenses.append(doc_dict)
    
    from app.services.excel_service import generate_excel
    excel_bytes = generate_excel(expenses)

    return StreamingResponse(
        io.BytesIO(excel_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=SmartTax_Report.xlsx"
        },
    )