# 🚀 SmartTax Assist - Complete Deployment Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [GitHub Setup](#github-setup)
3. [Backend Deployment (Render)](#backend-deployment-render)
4. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
5. [Environment Variables](#environment-variables)
6. [Post-Deployment Verification](#post-deployment-verification)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:
- ✅ A GitHub account (https://github.com)
- ✅ A Render account (https://render.com)
- ✅ A Vercel account (https://vercel.com)
- ✅ MongoDB Atlas cluster (https://cloud.mongodb.com)
- ✅ Git installed locally
- ✅ Node.js & npm installed

---

## GitHub Setup

### Step 1: Initialize Git Repository

If not already done:

```bash
cd /path/to/smart-tax-assist-v2
git init
```

### Step 2: Add All Files

```bash
git add .
```

**⚠️ IMPORTANT: Verify .env files are NOT included**

```bash
# Check git will ignore sensitive files
git status
```

You should NOT see:
- `.env`
- `.env.local`
- `backend/.env`
- `frontend/.env.local`

### Step 3: Create Initial Commit

```bash
git commit -m "Initial commit: SmartTax Assist application with environment variables configured"
```

### Step 4: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `smart-tax-assist-v2`
3. **IMPORTANT:** Set to **Private** (you can change to public later)
4. Do NOT initialize with README (you have one)
5. Click "Create repository"

### Step 5: Connect Local Repository to GitHub

Replace `YOUR_USERNAME` with your GitHub username:

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/smart-tax-assist-v2.git
git push -u origin main
```

### Step 6: Verify Upload

Visit `https://github.com/YOUR_USERNAME/smart-tax-assist-v2` to confirm all files are pushed.

---

## Backend Deployment (Render)

### Step 1: Create Render Account & Connect GitHub

1. Go to https://render.com
2. Sign up with GitHub (recommended - allows direct GitHub integration)
3. Click "New +" → "Web Service"
4. Select "Connect a repository"
5. Search for `smart-tax-assist-v2` and connect

### Step 2: Configure Backend Service

**Service Details:**
- **Name:** `smarttax-backend`
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- **Instance Type:** `Free` (or paid if needed)

### Step 3: Set Root Directory

- Root Directory: `backend`

### Step 4: Add Environment Variables

Click "Environment" and add:

```
MONGODB_URL = mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/smart_tax_assist?retryWrites=true&w=majority
JWT_SECRET = (generate strong secret: python -c "import secrets; print(secrets.token_urlsafe(32))")
ENVIRONMENT = production
PORT = 8000
```

**To get your MongoDB Atlas URL:**

1. Go to MongoDB Atlas: https://cloud.mongodb.com
2. Connect → Copy Connection String
3. Replace `<username>` and `<password>` with your Atlas credentials
4. Replace `/myFirstDatabase` with `/smart_tax_assist`

**Generate a strong JWT secret:**

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 5: Deploy

- Click "Create Web Service"
- Wait for build to complete (2-5 minutes)
- You'll get a URL like: `https://smarttax-backend.onrender.com`

### Step 6: Verify Backend Deployment

```bash
curl https://smarttax-backend.onrender.com/health
```

Expected response:
```json
{"status": "ok", "service": "SmartTax Assist API"}
```

---

## Frontend Deployment (Vercel)

### Step 1: Create Vercel Account & Import Project

1. Go to https://vercel.com
2. Sign up with GitHub (recommended)
3. Click "New Project" → "Import Git Repository"
4. Search for `smart-tax-assist-v2` and import

### Step 2: Configure Frontend

**Build Settings:**
- **Framework Preset:** Next.js
- **Root Directory:** `frontend`
- **Build Command:** `npm run build`
- **Install Command:** `npm install`
- **Output Directory:** `.next`

### Step 3: Add Environment Variables

Click "Environment Variables" and add:

```
NEXT_PUBLIC_API_URL = https://smart-tax-assist.onrender.com
NEXT_PUBLIC_ENVIRONMENT = production
```

**Production:** Set the environment to `Production`

### Step 4: Deploy

- Click "Deploy"
- Wait for build to complete (3-10 minutes)
- You'll get a URL like: `https://smart-tax-assist-v2.vercel.app`

### Step 5: Verify Frontend Deployment

- Visit `https://smart-tax-assist-v2.vercel.app`
- You should see the login page
- Try logging in or signing up

---

## Environment Variables

### Backend (.env for local development)

```env
MONGODB_URL=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/smart_tax_assist?retryWrites=true&w=majority
JWT_SECRET=your-super-secret-jwt-key
ENVIRONMENT=development
PORT=8000
```

### Frontend (.env.local for local development)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development
```

### Production Environment Variables

**Render (Backend):**
```
MONGODB_URL: <MongoDB Atlas URL>
JWT_SECRET: <Strong random key>
ENVIRONMENT: production
```

**Vercel (Frontend):**
```
NEXT_PUBLIC_API_URL: https://smart-tax-assist.onrender.com
NEXT_PUBLIC_ENVIRONMENT: production
```

---

## Post-Deployment Verification

### 1. Test API Health Endpoint

```bash
curl https://smarttax-backend.onrender.com/health
```

### 2. Test Frontend Accessibility

- Open https://smart-tax-assist-v2.vercel.app
- Should load without errors

### 3. Test Authentication Flow

1. Go to signup page
2. Create a test account
3. Login with the account
4. Upload a bill image
5. Verify data appears in dashboard

### 4. Check CORS Configuration

The backend should accept requests from Vercel frontend. If you see CORS errors:

1. Update CORS in `backend/app/main.py` to include Vercel URL
2. Redeploy backend

---

## Redeployment Steps

### When Code Changes

**Local:**
```bash
git add .
git commit -m "Describe your changes"
git push origin main
```

**Automatic Redeployment:**
- Render auto-deploys on push to main
- Vercel auto-deploys on push to main
- Wait 2-10 minutes for deployment

### When Environment Variables Change

**Render:**
1. Dashboard → Environment
2. Update variable
3. Click "Save Changes"
4. Redeploy manually or push to main

**Vercel:**
1. Settings → Environment Variables
2. Update variable
3. Redeploy manually: Project → Deployments → Click deployment → Redeploy

---

## Database Backup & Maintenance

### MongoDB Atlas Backups

1. Go to MongoDB Atlas → Cluster → Backup
2. Enable automated backups (recommended)
3. Snapshots saved for 7 days (free tier) or 35 days (paid)

### View Database in MongoDB Atlas

1. Go to MongoDB Atlas
2. Browse Collections
3. View `smart_tax_assist` database

---

## Troubleshooting

### ❌ Backend Not Starting on Render

**Check logs:**
1. Render Dashboard → Services → smarttax-backend
2. Click "Logs"
3. Look for error messages

**Common issues:**
- `ModuleNotFoundError`: Dependency not in `requirements.txt`
- `Connection refused`: MongoDB URL incorrect
- `CORS error`: Update CORS origins in code

**Solution:**
```bash
# Update requirements.txt locally
pip freeze > backend/requirements.txt
git push
# Render will auto-redeploy
```

### ❌ Frontend Not Loading on Vercel

**Check logs:**
1. Vercel Dashboard → Project → Deployments
2. Click failed deployment → Logs
3. Look for build errors

**Common issues:**
- TypeScript errors
- Missing environment variables
- Missing imports

**Solution:**
- Fix errors locally
- Test with `npm run build`
- Push to GitHub
- Vercel will redeploy

### ❌ API Calls Returning 404

**Problem:** Frontend can't reach backend

**Solution:**
1. Verify `NEXT_PUBLIC_API_URL` in Vercel environment variables
2. Ensure backend is running: `curl https://smart-tax-assist.onrender.com/health`
3. Check CORS in `backend/app/main.py`

### ❌ CORS Errors

**Error:** "Access to XMLHttpRequest blocked by CORS policy"

**Solution in backend/app/main.py:**

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://smart-tax-assist.vercel.app",  # Your Vercel frontend URL
        "https://*.vercel.app"  # Or allow all Vercel deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then:
```bash
git push
# Render will redeploy automatically
```

### ❌ MongoDB Connection Timeout

**Error:** "MongoNetworkError: connection timeout"

**Solution:**
1. Verify MongoDB URL is correct
2. Add Render IP to MongoDB Atlas whitelist:
   - MongoDB Atlas → Network Access
   - Add IP: `0.0.0.0/0` (allows all - not secure for production)
   - Or: Find Render server IP and whitelist that

### ⚠️ Lost Database

**MongoDB is reset:**
1. Re-create collections via migrations (if you have any)
2. Or manually create indexes:

```javascript
// In MongoDB Atlas console
db.users.createIndex({ email: 1 }, { unique: true })
db.expenses.createIndex({ user_id: 1 })
```

---

## Security Checklist

- ✅ .env files in .gitignore
- ✅ MongoDB username/password NOT in code
- ✅ JWT secret NOT in code (strong random key in Render)
- ✅ GitHub repository set to PRIVATE initially
- ✅ Render: Set service to Private (if available in paid tier)
- ✅ Vercel: Protect sensitive endpoints
- ✅ Update CORS to only allow your Vercel domain in production

---

## Support & Next Steps

### Issues?
1. Check Render logs: `https://dashboard.render.com/services`
2. Check Vercel logs: `https://vercel.com/dashboard`
3. Check MongoDB Atlas: `https://cloud.mongodb.com`

### To Disable Public Access
- Render: Settings → Private Service (paid plan)
- Vercel: Project Settings → Protection → Restrict to specific domains

### To Scale
- Render: Upgrade to paid tier for better performance
- Vercel: Already auto-scales with your plan
- MongoDB: Upgrade cluster tier on Atlas

---

**Deployment Complete! 🎉**

Your SmartTax Assist application is now live:
- 🌐 Frontend: `https://smart-tax-assist.vercel.app`
- 🔌 Backend: `https://smart-tax-assist.onrender.com`
- 🗄️ Database: `MongoDB Atlas`
