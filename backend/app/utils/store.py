# utils/store.py
# In-memory storage for expenses and categories (no database required)

from typing import Dict, List
from app.models.schemas import Expense

# ── Expenses stored by ID ────────────────────────────────────────────────────
expenses: Dict[str, Expense] = {}

# ── Default + user-defined categories ────────────────────────────────────────
categories: List[str] = [
    "Food",
    "Fuel",
    "Gas",
    "Education",
    "Travel",
    "Office Supplies",
    "Utilities",
    "Other",
]
