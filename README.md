# SmartTax Assist 🧾

A modern full-stack web application to upload bills, extract data via OCR, categorise expenses, and generate Excel tax reports.

---

## Architecture

```
smart-tax-assist/
├── backend/                  # FastAPI Python backend
│   ├── app/
│   │   ├── main.py           # App entry point + CORS
│   │   ├── routes/
│   │   │   ├── bills.py      # POST /upload-bill
│   │   │   ├── expenses.py   # GET/PUT/DELETE /expenses
│   │   │   ├── categories.py # CRUD /categories
│   │   │   └── export.py     # GET /export-excel
│   │   ├── services/
│   │   │   ├── ocr_service.py   # Tesseract OCR + field parsing
│   │   │   └── excel_service.py # OpenPyXL report generation
│   │   ├── models/
│   │   │   └── schemas.py    # Pydantic models
│   │   └── utils/
│   │       └── store.py      # In-memory expense/category store
│   └── requirements.txt
│
└── frontend/                 # Next.js 14 + Tailwind + TypeScript
    └── src/
        ├── app/
        │   ├── page.tsx           # Dashboard
        │   ├── upload/page.tsx    # Bill upload with drag-drop
        │   ├── expenses/page.tsx  # Editable expense table
        │   └── reports/page.tsx   # Excel report generation
        ├── components/
        │   └── layout/Sidebar.tsx
        └── lib/
            └── api.ts             # Typed API client
```

---

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | 3.10+   |
| Node.js     | 18+     |
| Tesseract   | 4.x+    |
| Poppler     | any     |

### Install system dependencies

**macOS:**
```bash
brew install tesseract poppler
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr poppler-utils
```

**Windows:**
- Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
- Poppler: https://github.com/oschwartz10612/poppler-windows/releases/

---

## Running the Backend

```bash
cd smart-tax-assist/backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate.bat       # Windows

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn app.main:app --reload --port 8000
```

API will be available at **http://localhost:8000**
Interactive docs at **http://localhost:8000/docs**

---

## Running the Frontend

```bash
cd smart-tax-assist/frontend

# Install Node dependencies
npm install

# Start the dev server
npm run dev
```

App will be available at **http://localhost:3000**

---

## API Reference

| Method | Endpoint              | Description                    |
|--------|-----------------------|--------------------------------|
| POST   | `/upload-bill`        | Upload bill, run OCR, extract  |
| GET    | `/expenses`           | List expenses (with filters)   |
| GET    | `/expenses/summary`   | Dashboard aggregate stats      |
| PUT    | `/expenses/{id}`      | Update category / type / etc.  |
| DELETE | `/expenses/{id}`      | Remove expense                 |
| GET    | `/categories`         | List categories                |
| POST   | `/categories`         | Add category                   |
| PUT    | `/categories/{name}`  | Rename category                |
| DELETE | `/categories/{name}`  | Delete category                |
| GET    | `/export-excel`       | Download SmartTax_Report.xlsx  |
| GET    | `/health`             | Health check                   |

---

## Features

### Bill Upload
- Drag-and-drop or click-to-browse upload
- JPG, PNG, PDF support (up to 10 MB)
- Tesseract OCR extracts: Vendor, Date, Total Amount, GST
- Bills processed **in-memory only** — never written to disk

### Expense Management
- Inline-editable table (vendor, category, expense type, amount)
- Filter by type (Personal/Business) and category
- Add, rename, delete custom categories
- Automatic category suggestions based on keyword matching

### Tax Calculation
- GST automatically detected and separated from total
- Summary view: total, GST, business vs personal splits

### Excel Export
- Two-sheet workbook: Expenses table + Summary
- Professional formatting with headers, alternating rows, totals
- Download via `GET /export-excel`

---

## Notes

- **No database** – all data is stored in-memory. Restarting the backend clears all data.
- **No authentication** – intended for local use.
- OCR quality depends on image clarity. Printed bills work best.
- If Tesseract is not installed, bills will be accepted but fields will default to 0/Unknown.
