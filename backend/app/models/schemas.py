# models/schemas.py
# Pydantic models for request/response validation

from pydantic import BaseModel
from typing import Optional
from datetime import date


class ExtractedBillData(BaseModel):
    """Data extracted from a bill via OCR."""
    vendor: str = "Unknown Vendor"
    bill_date: Optional[str] = None
    total_amount: float = 0.0
    gst_amount: float = 0.0
    raw_text: str = ""


class Expense(BaseModel):
    """Full expense record stored in memory."""
    id: str
    bill_name: str
    vendor: str
    category: str
    expense_type: str  # "Personal" or "Business"
    amount: float
    gst: float
    date: Optional[str] = None


class ExpenseUpdate(BaseModel):
    """Fields that can be updated on an expense."""
    category: Optional[str] = None
    expense_type: Optional[str] = None
    vendor: Optional[str] = None
    amount: Optional[float] = None
    gst: Optional[float] = None
    date: Optional[str] = None
    bill_name: Optional[str] = None


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    new_name: str


class SummaryStats(BaseModel):
    total_expenses: float
    total_gst: float
    business_expenses: float
    personal_expenses: float
    expense_count: int


# ==================== Authentication Models ====================

class SignupRequest(BaseModel):
    """Request for user signup."""
    email: str
    password: str
    full_name: str


class LoginRequest(BaseModel):
    """Request for user login."""
    email: str
    password: str


class UserResponse(BaseModel):
    """User information (excludes password)."""
    id: str
    email: str
    full_name: str


class TokenResponse(BaseModel):
    """Response with JWT token."""
    access_token: str
    token_type: str
    user: UserResponse


class TokenPayload(BaseModel):
    """Decoded JWT payload."""
    user_id: str
    exp: Optional[int] = None
