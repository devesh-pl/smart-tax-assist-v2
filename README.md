# SmartTax Assist 🧾

A modern full-stack web application to upload bills, extract data via OCR, categorise expenses, and generate Excel tax reports.

**NEW (v1.1):** Multi-user authentication with MongoDB database!

---

## Architecture

```
smart-tax-assist/
├── backend/                  # FastAPI Python backend + MongoDB
│   ├── app/
│   │   ├── main.py           # App entry point + CORS + DB init
│   │   ├── routes/
│   │   │   ├── auth.py       # POST /auth/signup, /login, /logout
│   │   │   ├── bills.py      # POST /upload-bill (authenticated)
│   │   │   ├── expenses.py   # GET/PUT/DELETE /expenses (user-isolated)
│   │   │   ├── categories.py # CRUD /categories (user-isolated)
│   │   │   └── export.py     # GET /export-excel (user-isolated)
│   │   ├── services/
│   │   │   ├── auth_service.py  # Password hashing, JWT tokens
│   │   │   ├── ocr_service.py   # Tesseract OCR + field parsing
│   │   │   └── excel_service.py # OpenPyXL report generation
│   │   ├── models/
│   │   │   └── schemas.py    # Pydantic models (including auth)
│   │   └── utils/
│   │       ├── db.py            # MongoDB connection utilities
│   │       ├── auth_dependency.py # JWT validation dependency
│   │       └── store.py         # Legacy in-memory store
│   ├── .env                  # MongoDB URL + JWT secret (user fills)
│   ├── .env.example          # Template
│   └── requirements.txt       # Updated with pymongo, bcrypt, PyJWT
│
└── frontend/                 # Next.js 14 + Tailwind + TypeScript
    └── src/
        ├── app/
        │   ├── page.tsx                  # Dashboard (protected)
        │   ├── auth/
        │   │   ├── signup/page.tsx      # User registration
        │   │   └── login/page.tsx       # User authentication
        │   ├── upload/page.tsx          # Bill upload (protected)
        │   ├── expenses/page.tsx        # Expense table (protected)
        │   └── reports/page.tsx         # Excel report (protected)
        ├── components/
        │   ├── layout/Sidebar.tsx       # Updated with user info + logout
        │   └── ProtectedRoute.tsx       # Route protection wrapper
        ├── context/
        │   └── AuthContext.tsx          # Global auth state
        ├── hooks/
        │   └── useAuth.ts               # Auth hook
        └── lib/
            └── api.ts                   # Typed API client (JWT integrated)
```

---

## What's New (v1.1)

✨ **User Authentication**
- Signup: Create account with email, name, password
- Login: Authenticate with email/password
- Logout: Clear session and token
- JWT-based: Secure token expiration (24 hours)

✨ **Data Isolation**
- Multi-user support: Each user sees only their own expenses
- User-specific categories: Custom categories per user
- Private data: No cross-user data leakage at API level

✨ **Persistent Database**
- MongoDB: Data persists across server restarts
- Cloud or Local: Supports MongoDB Atlas or local instances
- Secure: Passwords hashed with bcrypt, never stored plaintext

✨ **Protected Routes**
- Dashboard routes require authentication
- Auto-redirect to login if token missing/expired
- Automatic logout on 401 Unauthorized response

---

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | 3.10+   |
| Node.js     | 18+     |
| MongoDB     | 4.0+    |
| Tesseract   | 4.x+    |
| Poppler     | any     |

### MongoDB Setup

Choose one:

**Option A: MongoDB Atlas (Cloud - Recommended)**
1. Create free account at https://cloud.mongodb.com
2. Create a cluster
3. Get connection string: `mongodb+srv://user:pass@cluster.mongodb.net/...`

**Option B: Local MongoDB**
1. Install: https://docs.mongodb.com/manual/installation/
2. Start: `mongod`
3. Connection: `mongodb://localhost:27017`

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

## Quick Start

### Step 1: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate.bat       # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
# Edit .env and fill in:
# MONGODB_URL=your_mongodb_url
# JWT_SECRET=your_generated_secret (generate: python -c "import secrets; print(secrets.token_urlsafe(32))")

# Start server
python -m uvicorn app.main:app --reload --port 8000
```

### Step 2: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

### Step 3: Test

1. Open http://localhost:3000
2. Sign up with new credentials
3. Upload a bill
4. View dashboard and expenses

---

## API Reference

### Authentication (Public)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/signup` | Register new user |
| POST | `/auth/login` | Get JWT token |
| POST | `/auth/logout` | Invalidate token |

### Authentication (Protected)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/auth/me` | Get current user |

### Expenses (Protected, User-Isolated)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/expenses` | List user's expenses |
| GET | `/expenses/summary` | User's summary stats |
| POST | `/upload-bill` | Upload bill as user |
| PUT | `/expenses/{id}` | Update user's expense |
| DELETE | `/expenses/{id}` | Delete user's expense |

### Categories (Protected, User-Isolated)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categories` | Get user's categories |
| POST | `/categories` | Add category for user |
| PUT | `/categories/{name}` | Rename category |
| DELETE | `/categories/{name}` | Delete category |

### Export (Protected, User-Isolated)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/export-excel` | Download user's report |

### Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |

---

## Features

### User Authentication
- Email-based signup/login
- Bcrypt password hashing (12 rounds)
- JWT tokens (HS256, 24-hour expiration)
- Automatic logout on token expiration
- User info display in sidebar

### Bill Upload
- Drag-and-drop or click-to-browse upload
- JPG, PNG, PDF support (up to 10 MB)
- Tesseract OCR extracts: Vendor, Date, Total Amount, GST
- Bills processed in-memory — never written to disk

### Expense Management
- Inline-editable table (vendor, category, expense type, amount)
- Filter by type (Personal/Business) and category
- Add, rename, delete custom categories (per user)
- Automatic category suggestions based on keyword matching
- **User-isolated:** Each user sees only their own expenses

### Tax Calculation
- GST automatically detected and separated from total
- Summary view: total, GST, business vs personal splits
- **Per-user:** Summary calculated for current user only

### Excel Export
- Two-sheet workbook: Expenses table + Summary
- Professional formatting with headers, alternating rows, totals
- Download via `GET /export-excel`
- **User-isolated:** Only exports current user's data

---

## Database Schema

### Collections

**users** - User accounts
```json
{
  "_id": ObjectId,
  "email": "user@example.com",
  "full_name": "User Name",
  "password_hash": "$2b$12$...",
  "created_at": DateTime,
  "updated_at": DateTime
}
```

**expenses** - Expense records
```json
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "bill_name": "Receipt",
  "vendor": "Store",
  "category": "Food",
  "expense_type": "Personal|Business",
  "amount": 15.50,
  "gst": 1.55,
  "date": "2024-01-15",
  "created_at": DateTime,
  "updated_at": DateTime
}
```

**categories** - User categories
```json
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "name": "Groceries",
  "created_at": DateTime
}
```

---

## Security Features

✅ **Authentication**
- JWT-based with 24-hour expiration
- Secure token storage in browser localStorage
- Automatic logout on 401 responses

✅ **Password Security**
- Bcrypt hashing (12 salt rounds)
- Never stored in plaintext
- Verified on login

✅ **Data Isolation**
- All queries filtered by user_id at database level
- Cannot access another user's data via API
- Expenses, categories, exports all user-specific

✅ **CORS**
- Only localhost:3000 and 127.0.0.1:3000 allowed
- Prevents cross-origin attacks

---

## Documentation

For detailed setup, testing, and troubleshooting, see:
- **[QUICKSTART.md](QUICKSTART.md)** - Quick setup checklist
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed configuration
- **[DATABASE_DESIGN.md](DATABASE_DESIGN.md)** - MongoDB schema
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Complete overview
- **[FILE_INVENTORY.md](FILE_INVENTORY.md)** - All changed files

---

## Notes

- **v1.0:** Data was in-memory, lost on restart, single-user
- **v1.1:** Data persisted in MongoDB, multi-user, password-protected ✨
- OCR quality depends on image clarity. Printed bills work best.
- If Tesseract is not installed, bills will be accepted but fields will default to 0/Unknown.
- Requires MongoDB credentials (Atlas or local)
- Token expires after 24 hours (configured in `backend/.env`)

---

## Support

If you encounter issues:
1. Check [SETUP_GUIDE.md](SETUP_GUIDE.md) troubleshooting section
2. Verify MongoDB connection string
3. Ensure all dependencies installed: `pip install -r requirements.txt`
4. Check browser console (F12) for frontend errors
5. Check terminal output for backend errors

---

**Version:** 1.1.0 (with Authentication & MongoDB)  
**Last Updated:** May 6, 2026

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

- **v1.0:** Data was in-memory, lost on restart, single-user
- **v1.1:** Data persisted in MongoDB, multi-user, password-protected ✨
- OCR quality depends on image clarity. Printed bills work best.
- If Tesseract is not installed, bills will be accepted but fields will default to 0/Unknown.
- Requires MongoDB credentials (Atlas or local)
- Token expires after 24 hours (configured in `backend/.env`)

---

## Support

If you encounter issues:
1. Check [SETUP_GUIDE.md](SETUP_GUIDE.md) troubleshooting section
2. Verify MongoDB connection string
3. Ensure all dependencies installed: `pip install -r requirements.txt`
4. Check browser console (F12) for frontend errors
5. Check terminal output for backend errors

---

**Version:** 1.1.0 (with Authentication & MongoDB)  
**Last Updated:** May 6, 2026
