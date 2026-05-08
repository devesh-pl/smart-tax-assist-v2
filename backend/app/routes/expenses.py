# routes/expenses.py
# GET /expenses  |  PUT /expenses/{id}  |  DELETE /expenses/{id}
# GET /expenses/summary

from fastapi import APIRouter, HTTPException, Depends, status
from typing import Optional
from bson.objectid import ObjectId

from app.models.schemas import ExpenseUpdate, SummaryStats, Expense
from app.utils.db import get_expenses_collection
from app.utils.auth_dependency import get_current_user

router = APIRouter()


@router.get("/expenses")
async def get_expenses(
    category: Optional[str] = None,
    expense_type: Optional[str] = None,
    month: Optional[str] = None,          # "YYYY-MM"
    current_user: dict = Depends(get_current_user),
):
    """
    Return all expenses for current user with optional filters:
      - category   : exact match
      - expense_type : "Personal" | "Business"
      - month      : "YYYY-MM" prefix match on date field
    """
    expenses_col = get_expenses_collection()
    
    # Build query for current user
    query = {"user_id": ObjectId(current_user["_id"])}
    
    if category:
        query["category"] = {"$regex": f"^{category}$", "$options": "i"}
    if expense_type:
        query["expense_type"] = {"$regex": f"^{expense_type}$", "$options": "i"}
    if month:
        query["date"] = {"$regex": f"^{month}"}
    
    # Query and format results
    results = []
    for doc in expenses_col.find(query):
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        doc["user_id"] = str(doc["user_id"])  # Convert user_id to string too
        results.append(doc)
    
    return results

@router.get("/expenses/summary")
async def get_summary(current_user: dict = Depends(get_current_user)) -> SummaryStats:
    """Aggregate stats for current user used by the dashboard."""
    expenses_col = get_expenses_collection()
    
    # Get all expenses for current user
    query = {"user_id": ObjectId(current_user["_id"])}
    all_expenses = list(expenses_col.find(query))
    
    return SummaryStats(
        total_expenses=sum(e.get("amount", 0) for e in all_expenses),
        total_gst=sum(e.get("gst", 0) for e in all_expenses),
        business_expenses=sum(e.get("amount", 0) for e in all_expenses if e.get("expense_type") == "Business"),
        personal_expenses=sum(e.get("amount", 0) for e in all_expenses if e.get("expense_type") == "Personal"),
        expense_count=len(all_expenses),
    )


@router.put("/expenses/{expense_id}")
async def update_expense(
    expense_id: str,
    payload: ExpenseUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Patch mutable fields on an expense (only if owned by current user)."""
    expenses_col = get_expenses_collection()
    
    try:
        obj_id = ObjectId(expense_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid expense ID.")
    
    # Check ownership
    expense = expenses_col.find_one({
        "_id": obj_id,
        "user_id": ObjectId(current_user["_id"])
    })
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found.")
    
    # Update only set fields
    update_data = payload.model_dump(exclude_unset=True)
    if update_data:
        expenses_col.update_one(
            {"_id": obj_id},
            {"$set": update_data}
        )
    
    # Return updated expense
    updated = expenses_col.find_one({"_id": obj_id})
    updated["id"] = str(updated["_id"])
    return updated


@router.delete("/expenses/{expense_id}")
async def delete_expense(
    expense_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Remove an expense (only if owned by current user)."""
    expenses_col = get_expenses_collection()
    
    try:
        obj_id = ObjectId(expense_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid expense ID.")
    
    # Check ownership and delete
    result = expenses_col.delete_one({
        "_id": obj_id,
        "user_id": ObjectId(current_user["_id"])
    })
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found.")
    
    return {"message": "Expense deleted.", "id": expense_id}
