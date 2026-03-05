# routes/export.py
# GET /export-excel  –  stream a generated Excel workbook

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import io

from app.services.excel_service import generate_excel
from app.utils import store

router = APIRouter()


@router.get("/export-excel")
def export_excel():
    """Generate and stream an Excel file of all stored expenses."""
    expenses = list(store.expenses.values())
    excel_bytes = generate_excel(expenses)

    return StreamingResponse(
        io.BytesIO(excel_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=SmartTax_Report.xlsx"
        },
    )
