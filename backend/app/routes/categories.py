# routes/categories.py
# CRUD for custom expense categories (MongoDB-backed)

from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from bson.objectid import ObjectId

from app.models.schemas import CategoryCreate, CategoryUpdate
from app.utils.db import get_categories_collection
from app.utils.auth_dependency import get_current_user

router = APIRouter()


@router.get("/categories")
async def get_categories(current_user: dict = Depends(get_current_user)):
    """Get all categories for current user."""
    categories_col = get_categories_collection()
    
    # Get default categories + user's custom categories
    default_categories = [
        "Food", "Fuel", "Gas", "Education", "Travel", 
        "Office Supplies", "Utilities", "Other"
    ]
    
    # Get user's custom categories
    custom_cats = list(categories_col.find(
        {"user_id": ObjectId(current_user["_id"])}
    ))
    custom_names = [cat["name"] for cat in custom_cats]
    
    # Combine default and custom (remove duplicates)
    all_categories = list(dict.fromkeys(default_categories + custom_names))
    
    return {"categories": all_categories}


@router.post("/categories")
async def add_category(
    payload: CategoryCreate,
    current_user: dict = Depends(get_current_user),
):
    """Add a custom category for current user."""
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Category name cannot be empty.")
    
    categories_col = get_categories_collection()
    
    # Check if category already exists for this user
    existing = categories_col.find_one({
        "user_id": ObjectId(current_user["_id"]),
        "name": name
    })
    if existing:
        raise HTTPException(status_code=409, detail="Category already exists.")
    
    # Insert new category
    now = datetime.utcnow()
    category_doc = {
        "user_id": ObjectId(current_user["_id"]),
        "name": name,
        "created_at": now,
    }
    categories_col.insert_one(category_doc)
    
    # Return all categories
    custom_cats = list(categories_col.find(
        {"user_id": ObjectId(current_user["_id"])}
    ))
    custom_names = [cat["name"] for cat in custom_cats]
    
    default_categories = [
        "Food", "Fuel", "Gas", "Education", "Travel", 
        "Office Supplies", "Utilities", "Other"
    ]
    all_categories = list(dict.fromkeys(default_categories + custom_names))
    
    return {"categories": all_categories}


@router.put("/categories/{category_name}")
async def rename_category(
    category_name: str,
    payload: CategoryUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Rename a custom category (only if owned by current user)."""
    new_name = payload.new_name.strip()
    if not new_name:
        raise HTTPException(status_code=400, detail="New name cannot be empty.")
    
    categories_col = get_categories_collection()
    
    # Find and update category (only if owned by user)
    result = categories_col.update_one(
        {
            "user_id": ObjectId(current_user["_id"]),
            "name": category_name
        },
        {"$set": {"name": new_name}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Category not found.")
    
    # Return all categories
    custom_cats = list(categories_col.find(
        {"user_id": ObjectId(current_user["_id"])}
    ))
    custom_names = [cat["name"] for cat in custom_cats]
    
    default_categories = [
        "Food", "Fuel", "Gas", "Education", "Travel", 
        "Office Supplies", "Utilities", "Other"
    ]
    all_categories = list(dict.fromkeys(default_categories + custom_names))
    
    return {"categories": all_categories}


@router.delete("/categories/{category_name}")
async def delete_category(
    category_name: str,
    current_user: dict = Depends(get_current_user),
):
    """Delete a custom category (only if owned by current user)."""
    categories_col = get_categories_collection()
    
    # Delete category (only if owned by user)
    result = categories_col.delete_one({
        "user_id": ObjectId(current_user["_id"]),
        "name": category_name
    })
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found.")
    
    # Return all categories
    custom_cats = list(categories_col.find(
        {"user_id": ObjectId(current_user["_id"])}
    ))
    custom_names = [cat["name"] for cat in custom_cats]
    
    default_categories = [
        "Food", "Fuel", "Gas", "Education", "Travel", 
        "Office Supplies", "Utilities", "Other"
    ]
    all_categories = list(dict.fromkeys(default_categories + custom_names))
    
    return {"categories": all_categories}
