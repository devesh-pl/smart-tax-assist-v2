# app/main.py
# SmartTax Assist – FastAPI application entry point

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import bills, expenses, categories, export, auth
from app.utils.db import init_db, close_db
from app.services import auth_service

# ── Load environment variables ────────────────────────────────────────────────
load_dotenv()

app = FastAPI(
    title="SmartTax Assist API",
    description="Backend API for bill OCR, expense tracking, and tax report generation.",
    version="1.0.0",
)

# ── CORS Configuration ───────────────────────────────────────────────────────
# Different CORS rules for development vs production
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT == "production":
    # Production: Only allow specific Vercel domain(s)
    ALLOWED_ORIGINS = [
        "https://smart-tax-assist.vercel.app",    # Your actual Vercel URL
        "https://smart-tax-assist-v2.vercel.app",  # If you deploy to this too
    ]
else:
    # Development: Allow localhost
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Startup and Shutdown Events ──────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup."""
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017/smart_tax_assist")
    jwt_secret = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
    
    init_db(mongodb_url)
    auth_service.set_jwt_secret(jwt_secret)
    print(f"✓ Application startup complete (Environment: {ENVIRONMENT})")

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown."""
    close_db()
    print("✓ Application shutdown complete")

# ── Routers ──────────────────────────────────────────────────────────────────
app.include_router(auth.router,       tags=["Auth"])
app.include_router(bills.router,      tags=["Bills"])
app.include_router(expenses.router,   tags=["Expenses"])
app.include_router(categories.router, tags=["Categories"])
app.include_router(export.router,     tags=["Export"])


@app.get("/", tags=["Root"])
def root():
    """Root endpoint - confirms server is running."""
    return {
        "message": "SmartTax Assist Backend Server Running Successfully",
        "service": "SmartTax Assist API",
        "version": "1.0.0",
        "status": "running",
        "environment": ENVIRONMENT
    }


@app.get("/health", tags=["Health"])
def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "SmartTax Assist API",
        "environment": ENVIRONMENT
    }
