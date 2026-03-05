# routes/categories.py
# CRUD for custom expense categories (in-memory)

from fastapi import APIRouter, HTTPException
from app.models.schemas import CategoryCreate, CategoryUpdate
from app.utils import store

router = APIRouter()


@router.get("/categories")
def get_categories():
    return {"categories": store.categories}


@router.post("/categories")
def add_category(payload: CategoryCreate):
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Category name cannot be empty.")
    if name in store.categories:
        raise HTTPException(status_code=409, detail="Category already exists.")
    store.categories.append(name)
    return {"categories": store.categories}


@router.put("/categories/{category_name}")
def rename_category(category_name: str, payload: CategoryUpdate):
    new_name = payload.new_name.strip()
    if category_name not in store.categories:
        raise HTTPException(status_code=404, detail="Category not found.")
    if not new_name:
        raise HTTPException(status_code=400, detail="New name cannot be empty.")
    idx = store.categories.index(category_name)
    store.categories[idx] = new_name
    # Also update any expenses that used the old category name
    for exp in store.expenses.values():
        if exp.category == category_name:
            exp.category = new_name
    return {"categories": store.categories}


@router.delete("/categories/{category_name}")
def delete_category(category_name: str):
    if category_name not in store.categories:
        raise HTTPException(status_code=404, detail="Category not found.")
    store.categories.remove(category_name)
    return {"categories": store.categories}
