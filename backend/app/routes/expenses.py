# routes/expenses.py
# GET /expenses  |  PUT /expenses/{id}  |  DELETE /expenses/{id}
# GET /expenses/summary

from fastapi import APIRouter, HTTPException
from typing import Optional

from app.models.schemas import ExpenseUpdate, SummaryStats
from app.utils import store

router = APIRouter()


@router.get("/expenses")
def get_expenses(
    category: Optional[str] = None,
    expense_type: Optional[str] = None,
    month: Optional[str] = None,          # "YYYY-MM"
):
    """
    Return all stored expenses with optional filters:
      - category   : exact match
      - expense_type : "Personal" | "Business"
      - month      : "YYYY-MM" prefix match on date field
    """
    results = list(store.expenses.values())

    if category:
        results = [e for e in results if e.category.lower() == category.lower()]
    if expense_type:
        results = [e for e in results if e.expense_type.lower() == expense_type.lower()]
    if month:
        results = [e for e in results if e.date and e.date.startswith(month)]

    return [e.model_dump() for e in results]


@router.get("/expenses/summary")
def get_summary() -> SummaryStats:
    """Aggregate stats used by the dashboard."""
    all_exp = list(store.expenses.values())
    return SummaryStats(
        total_expenses=sum(e.amount for e in all_exp),
        total_gst=sum(e.gst for e in all_exp),
        business_expenses=sum(e.amount for e in all_exp if e.expense_type == "Business"),
        personal_expenses=sum(e.amount for e in all_exp if e.expense_type == "Personal"),
        expense_count=len(all_exp),
    )


@router.put("/expenses/{expense_id}")
def update_expense(expense_id: str, payload: ExpenseUpdate):
    """Patch mutable fields on a stored expense."""
    expense = store.expenses.get(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found.")

    updated = expense.model_dump()
    for field, value in payload.model_dump(exclude_unset=True).items():
        updated[field] = value

    from app.models.schemas import Expense
    store.expenses[expense_id] = Expense(**updated)
    return store.expenses[expense_id].model_dump()


@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: str):
    """Remove an expense from the in-memory store."""
    if expense_id not in store.expenses:
        raise HTTPException(status_code=404, detail="Expense not found.")
    del store.expenses[expense_id]
    return {"message": "Expense deleted.", "id": expense_id}
