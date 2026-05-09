# app/main.py
# SmartTax Assist – FastAPI application entry point

import os
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import bills, expenses, categories, export, auth
from app.utils.db import init_db, close_db
from app.services import auth_service

# ── Metrics (simple in-memory tracking) ──────────────────────────────────────
class Metrics:
    def __init__(self):
        self.start_time = datetime.utcnow()
        self.total_requests = 0
        self.errors = 0
    
    def increment_requests(self):
        self.total_requests += 1
    
    def increment_errors(self):
        self.errors += 1
    
    def get_uptime_seconds(self):
        return (datetime.utcnow() - self.start_time).total_seconds()

metrics = Metrics()

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
        "https://smart-tax-assist.vercel.app",    # Your Vercel frontend
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

# ── Request Tracking Middleware ──────────────────────────────────────────────
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        metrics.increment_requests()
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            metrics.increment_errors()
            raise

app.add_middleware(MetricsMiddleware)

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


@app.get("/metrics", tags=["Metrics"])
def get_metrics():
    """Application metrics endpoint."""
    return {
        "status": "ok",
        "service": "SmartTax Assist API",
        "environment": ENVIRONMENT,
        "uptime_seconds": metrics.get_uptime_seconds(),
        "total_requests": metrics.total_requests,
        "error_count": metrics.errors,
        "timestamp": datetime.utcnow().isoformat()
    }
