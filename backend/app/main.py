# app/main.py
# SmartTax Assist – FastAPI application entry point

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import bills, expenses, categories, export

app = FastAPI(
    title="SmartTax Assist API",
    description="Backend API for bill OCR, expense tracking, and tax report generation.",
    version="1.0.0",
)

# ── CORS – allow the Next.js dev server ──────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──────────────────────────────────────────────────────────────────
app.include_router(bills.router,      tags=["Bills"])
app.include_router(expenses.router,   tags=["Expenses"])
app.include_router(categories.router, tags=["Categories"])
app.include_router(export.router,     tags=["Export"])


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "service": "SmartTax Assist API"}
