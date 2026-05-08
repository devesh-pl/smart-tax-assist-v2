# 🌍 Environment Variables Setup Guide

## Overview

This guide explains how to configure environment variables for different deployment scenarios.

---

## Local Development Setup

### Backend Setup

#### Step 1: Copy Example File

```bash
cd backend
cp .env.example .env
```

#### Step 2: Edit `.env` File

```bash
# backend/.env
MONGODB_URL=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/smart_tax_assist?retryWrites=true&w=majority
JWT_SECRET=your-development-secret-key
JWT_EXPIRATION_HOURS=24
ENVIRONMENT=development
PORT=8000
```

#### Step 3: Get MongoDB Atlas URL

1. Go to https://cloud.mongodb.com
2. Clusters → Connect → Connect your application
3. Copy connection string
4. Replace `<username>` and `<password>` with your credentials
5. Replace `/myFirstDatabase` with `/smart_tax_assist`

Example:
```
mongodb+srv://darshanjss71_db_user:0fZ4fWWipy5mMnt6@cluster0.xcwmbff.mongodb.net/smart_tax_assist?retryWrites=true&w=majority
```

#### Step 4: Run Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Run with uvicorn
uvicorn app.main:app --reload

# Or with Python
python -m uvicorn app.main:app --reload
```

✅ Backend running at: `http://localhost:8000`

---

### Frontend Setup

#### Step 1: Copy Example File

```bash
cd frontend
cp .env.local.example .env.local
```

#### Step 2: Edit `.env.local` File

```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development
```

#### Step 3: Install Dependencies

```bash
npm install
```

#### Step 4: Run Frontend

```bash
npm run dev
```

✅ Frontend running at: `http://localhost:3000`

---

## Docker Local Development

### Build & Run with Docker Compose

#### Step 1: Create `.env.local` in Project Root

```bash
# .env.local (in project root)
MONGODB_URL=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/smart_tax_assist
JWT_SECRET=your-secret-key-for-development
NEXT_PUBLIC_API_URL=http://localhost:8000
ENVIRONMENT=development
```

#### Step 2: Run Docker Compose

```bash
docker-compose up --build
```

#### Step 3: Access Services

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`

#### Step 4: Stop Services

```bash
docker-compose down
```

---

## Production Deployment

### Render Backend Deployment

#### Step 1: Connect GitHub Repository

1. Go to https://render.com
2. New → Web Service
3. Select your GitHub repository
4. Select `main` branch

#### Step 2: Configure Service

- **Name:** `smarttax-backend`
- **Environment:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- **Root Directory:** `backend`

#### Step 3: Add Environment Variables

Click "Environment" and add:

| Key | Value | Notes |
|-----|-------|-------|
| `MONGODB_URL` | `mongodb+srv://...` | Your MongoDB Atlas URL |
| `JWT_SECRET` | `<strong random key>` | Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `ENVIRONMENT` | `production` | Must be `production` |
| `PORT` | `8000` | Render will override automatically |

#### Step 4: Deploy

- Click "Create Web Service"
- Wait 2-5 minutes
- You'll get URL: `https://smarttax-backend.onrender.com`

---

### Vercel Frontend Deployment

#### Step 1: Import GitHub Repository

1. Go to https://vercel.com
2. New Project → Import Git Repository
3. Select your repository

#### Step 2: Configure Project

- **Framework:** Next.js
- **Root Directory:** `frontend`
- **Build Command:** `npm run build`
- **Install Command:** `npm install`

#### Step 3: Add Environment Variables

Click "Environment Variables" and add:

| Key | Value | Notes |
|-----|-------|-------|
| `NEXT_PUBLIC_API_URL` | `https://smarttax-backend.onrender.com` | Your Render backend URL |
| `NEXT_PUBLIC_ENVIRONMENT` | `production` | Must be `production` |

#### Step 4: Deploy

- Click "Deploy"
- Wait 3-10 minutes
- You'll get URL: `https://smart-tax-assist-v2.vercel.app`

---

## Environment Variable Reference

### Backend (.env / Render)

| Variable | Type | Required | Default | Example |
|----------|------|----------|---------|---------|
| `MONGODB_URL` | String | ✅ Yes | - | `mongodb+srv://user:pass@cluster...` |
| `JWT_SECRET` | String | ✅ Yes | - | `super-secret-key-32-chars-min` |
| `JWT_EXPIRATION_HOURS` | Number | ❌ No | `24` | `24` |
| `ENVIRONMENT` | String | ❌ No | `development` | `production` or `development` |
| `PORT` | Number | ❌ No | `8000` | `8000` |

### Frontend (.env.local / Vercel)

| Variable | Type | Required | Default | Example | Public |
|----------|------|----------|---------|---------|--------|
| `NEXT_PUBLIC_API_URL` | String | ✅ Yes | - | `http://localhost:8000` | ✅ Yes |
| `NEXT_PUBLIC_ENVIRONMENT` | String | ❌ No | `development` | `production` | ✅ Yes |

**Note:** Only variables prefixed with `NEXT_PUBLIC_` are exposed to the browser!

---

## How Environment Variables Are Loaded

### Backend

```python
# In app/main.py
import os
from dotenv import load_dotenv

# Loads .env file
load_dotenv()

# Access variables
mongodb_url = os.getenv("MONGODB_URL", "default-value")
jwt_secret = os.getenv("JWT_SECRET", "default-secret")
```

**Loading order:**
1. System environment variables
2. `.env` file (local development)
3. Default values in code

### Frontend (Next.js)

```javascript
// In frontend/.env.local or Vercel Environment Variables
NEXT_PUBLIC_API_URL=http://localhost:8000

// Access in code
const apiUrl = process.env.NEXT_PUBLIC_API_URL
```

**Loading order:**
1. `.env.local` (local development)
2. Vercel Environment Variables (production)
3. `.env` (fallback)

---

## Docker Environment Variables

### docker-compose.yml

```yaml
services:
  backend:
    environment:
      MONGODB_URL: ${MONGODB_URL}
      JWT_SECRET: ${JWT_SECRET}
      ENVIRONMENT: ${ENVIRONMENT:-development}
    env_file:
      - .env.local
```

**How it works:**
1. Reads from `.env.local` file
2. Can be overridden by shell environment
3. `${VAR:-default}` means use default if not set

### Example .env.local for Docker

```env
MONGODB_URL=mongodb+srv://user:pass@cluster...
JWT_SECRET=secret-key
NEXT_PUBLIC_API_URL=http://localhost:8000
ENVIRONMENT=development
```

---

## Common Scenarios

### Scenario 1: Local Development

```bash
# backend/.env
MONGODB_URL=mongodb+srv://user:pass@cluster...
JWT_SECRET=dev-secret-key
ENVIRONMENT=development

# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Run:
```bash
# Terminal 1
cd backend && uvicorn app.main:app --reload

# Terminal 2
cd frontend && npm run dev
```

### Scenario 2: Docker Local Development

```bash
# .env.local (project root)
MONGODB_URL=mongodb+srv://user:pass@cluster...
JWT_SECRET=dev-secret-key
NEXT_PUBLIC_API_URL=http://localhost:8000
ENVIRONMENT=development
```

Run:
```bash
docker-compose up --build
```

### Scenario 3: Production (Render + Vercel)

**Render Backend:**
```
MONGODB_URL = mongodb+srv://user:pass@cluster...
JWT_SECRET = <strong-random-32-char-key>
ENVIRONMENT = production
```

**Vercel Frontend:**
```
NEXT_PUBLIC_API_URL = https://smarttax-backend.onrender.com
NEXT_PUBLIC_ENVIRONMENT = production
```

---

## Generating Strong Secrets

### JWT Secret

```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -base64 32

# Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

### MongoDB Password

- Use MongoDB Atlas built-in password generator
- Minimum 8 characters
- Include: Uppercase, lowercase, numbers, symbols

---

## Testing Environment Variables

### Backend

```bash
# Check if .env is loaded
python -c "
import os
from dotenv import load_dotenv
load_dotenv('backend/.env')
print(f'MONGODB_URL: {os.getenv(\"MONGODB_URL\", \"NOT SET\")}')
print(f'JWT_SECRET: {os.getenv(\"JWT_SECRET\", \"NOT SET\")}')
print(f'ENVIRONMENT: {os.getenv(\"ENVIRONMENT\", \"NOT SET\")}')
"
```

### Frontend

```bash
# Check if .env.local is loaded
cd frontend
npm run dev

# Check in browser console
console.log(process.env.NEXT_PUBLIC_API_URL)
```

---

## Troubleshooting

### ❌ "MONGODB_URL not found"

**Cause:** `.env` file not in correct directory

**Solution:**
```bash
# Should be in backend/ directory
ls backend/.env

# If not present
cp backend/.env.example backend/.env
# Edit with your values
```

### ❌ "API_URL is undefined"

**Cause:** Frontend can't find `NEXT_PUBLIC_API_URL`

**Solution:**
```bash
# Should be in frontend/ directory
ls frontend/.env.local

# If not present
cp frontend/.env.local.example frontend/.env.local
# Edit with your backend URL
```

### ❌ "Connection refused" in Production

**Cause:** `NEXT_PUBLIC_API_URL` incorrect or backend not running

**Solution:**
1. Verify Render URL is correct
2. Test backend: `curl https://smarttax-backend.onrender.com/health`
3. Update Vercel environment variable
4. Redeploy Vercel

### ❌ "Docker can't find environment variables"

**Cause:** `.env.local` not in project root

**Solution:**
```bash
# Create in project root (not in backend or frontend)
cat > .env.local << EOF
MONGODB_URL=mongodb+srv://...
JWT_SECRET=secret-key
NEXT_PUBLIC_API_URL=http://localhost:8000
ENVIRONMENT=development
EOF

# Run docker-compose
docker-compose up
```

---

## Security Reminders

✅ **DO:**
- Store secrets in environment variables
- Use `.env.example` for reference only
- Keep `.env*` in `.gitignore`
- Use strong random secrets (32+ characters)
- Rotate secrets periodically

❌ **DON'T:**
- Hardcode secrets in code
- Commit `.env` files to GitHub
- Share secrets in messages/emails
- Use simple passwords
- Reuse secrets across environments

---

## Migration from Hardcoded to Environment Variables

If your code previously had hardcoded values:

### Step 1: Identify Hardcoded Values

```bash
grep -r "mongodb\+srv" backend/
grep -r "JWT_SECRET\|jwt_secret" backend/
grep -r "password" backend/
```

### Step 2: Update Code

**Before:**
```python
MONGODB_URL = "mongodb+srv://user:pass@cluster..."
JWT_SECRET = "hardcoded-secret"
```

**After:**
```python
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/smart_tax_assist")
JWT_SECRET = os.getenv("JWT_SECRET", "change-me-in-production")
```

### Step 3: Update .gitignore

```bash
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
```

### Step 4: Commit & Push

```bash
git add .
git commit -m "feat: move secrets to environment variables"
git push origin main
```

---

**✅ Your environment is now properly secured!**

Next steps:
1. ✅ Set up local `.env` files
2. ✅ Deploy to Render (add Render env vars)
3. ✅ Deploy to Vercel (add Vercel env vars)
4. ✅ Test both deployments
5. ✅ Push to GitHub (no secrets!)
