# ⚡ Quick Start Deployment Checklist

## Pre-Deployment (5 minutes)

```bash
# 1. Verify no secrets in git
grep -r "mongodb+srv" . --exclude-dir=.git --exclude-dir=node_modules
grep -r "JWT_SECRET" . --exclude-dir=.git --exclude-dir=node_modules --exclude="*.md"

# 2. Create .env files locally (NOT committed)
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local

# 3. Edit with your values (in .env files, NOT in code)
# backend/.env:
#   MONGODB_URL=your-mongodb-atlas-url
#   JWT_SECRET=generate-strong-secret
#   ENVIRONMENT=development

# frontend/.env.local:
#   NEXT_PUBLIC_API_URL=http://localhost:8000
#   NEXT_PUBLIC_ENVIRONMENT=development

# 4. Verify .gitignore includes .env files
grep ".env" .gitignore

# 5. Stage and commit (NO .env files!)
git add .
git status  # Verify NO .env files shown
git commit -m "Setup: Configure for deployment"
```

---

## GitHub Push (5 minutes)

```bash
# 1. Create GitHub repository
# https://github.com/new → Create repo → Copy URL

# 2. Connect and push
git remote add origin https://github.com/YOUR_USERNAME/smart-tax-assist-v2.git
git branch -M main
git push -u origin main

# 3. Verify on GitHub
# Visit https://github.com/YOUR_USERNAME/smart-tax-assist-v2
# Confirm: All files present, NO .env files visible
```

---

## Backend Deployment to Render (10 minutes)

```bash
# 1. Go to https://render.com → New → Web Service
# 2. Connect GitHub repository
# 3. Configure:
#    Name: smarttax-backend
#    Environment: Python 3
#    Build: pip install -r requirements.txt
#    Start: uvicorn app.main:app --host 0.0.0.0 --port 8000
#    Root: backend

# 4. Add Environment Variables:
MONGODB_URL=mongodb+srv://USERNAME:PASSWORD@cluster0.xxxxx.mongodb.net/smart_tax_assist?retryWrites=true&w=majority
JWT_SECRET=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
ENVIRONMENT=production

# 5. Click "Create Web Service"
# 6. Wait 2-5 minutes, get URL: https://smarttax-backend.onrender.com

# 7. Test
curl https://smarttax-backend.onrender.com/health
# Should return: {"status":"ok","service":"SmartTax Assist API"}
```

---

## Frontend Deployment to Vercel (10 minutes)

```bash
# 1. Go to https://vercel.com → New Project → Import Git Repository
# 2. Select repository
# 3. Configure:
#    Framework: Next.js
#    Root: frontend
#    Build: npm run build
#    Install: npm install

# 4. Add Environment Variables:
NEXT_PUBLIC_API_URL=https://smarttax-backend.onrender.com
NEXT_PUBLIC_ENVIRONMENT=production

# 5. Click "Deploy"
# 6. Wait 3-10 minutes, get URL: https://smart-tax-assist-v2.vercel.app

# 7. Test
# Visit https://smart-tax-assist-v2.vercel.app
# You should see login page
```

---

## Post-Deployment Verification (5 minutes)

```bash
# 1. Backend health check
curl https://smarttax-backend.onrender.com/health

# 2. Frontend accessibility
# Open https://smart-tax-assist-v2.vercel.app

# 3. Test signup/login flow
# - Go to signup
# - Create test account
# - Login
# - Upload bill

# 4. Check CORS (if errors, update backend CORS config)
# Error? → Update backend/app/main.py CORS → Push → Render redeploys
```

---

## For Future Code Changes

```bash
# 1. Make code changes locally
# 2. Test: npm run dev (frontend), python -m uvicorn ... (backend)
# 3. Commit: git add . && git commit -m "description"
# 4. Push: git push origin main
# 5. Auto-redeploys:
#    - Render: 2 minutes
#    - Vercel: 3 minutes
```

---

## Emergency: Secrets Exposed?

```bash
# 1. Rotate credentials IMMEDIATELY:
#    - MongoDB Atlas → Change password
#    - Render → Update JWT_SECRET
#    - Vercel → Redeploy

# 2. Remove from git history (if not yet public):
git rm --cached backend/.env
git add .gitignore
git commit --amend --no-edit
git push origin main --force

# 3. If already public: Assume compromised, rotate all secrets
```

---

## Common Issues

### ❌ CORS Error
```bash
# Update backend/app/main.py with Vercel URL
# Redeploy (git push)
```

### ❌ API Returns 404
```bash
# 1. Check Vercel env var: NEXT_PUBLIC_API_URL
# 2. Check backend running: curl https://smarttax-backend.onrender.com/health
# 3. Redeploy Vercel
```

### ❌ Database Connection Error
```bash
# 1. Verify MONGODB_URL in Render env vars
# 2. Add Render IP to MongoDB Atlas whitelist (0.0.0.0/0 for testing)
# 3. Redeploy backend
```

---

## URLs After Deployment

```
Frontend: https://smart-tax-assist-v2.vercel.app
Backend: https://smarttax-backend.onrender.com
GitHub: https://github.com/YOUR_USERNAME/smart-tax-assist-v2
```

---

## Important Reminders

✅ **Must Do:**
- Store secrets in `.env` files ONLY
- Add `.env*` to `.gitignore`
- Use strong JWT secrets (32+ characters)
- Set `ENVIRONMENT=production` for Render

❌ **Never Do:**
- Commit `.env` files
- Hardcode secrets in code
- Share credentials in messages
- Use same secrets for dev and prod

---

**Done! Your app is deployed! 🎉**
