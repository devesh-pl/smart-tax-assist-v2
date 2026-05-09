# 🚀 DevOps Setup & CI/CD Pipeline Guide

## Overview

Your SmartTax Assist v2 project now includes a comprehensive DevOps pipeline:
- **CI Pipeline** (`ci.yml`): Runs on every push/PR - lints, tests, builds Docker images
- **CD Pipeline** (`cd.yml`): Runs on main branch push - automatically deploys to Render (backend) and Vercel (frontend)

---

## Quick Start (5 minutes)

### Step 1: Configure GitHub Secrets

Your CI/CD workflows need authentication credentials. Add these to your GitHub repository:

1. Go to: `GitHub Repo → Settings → Secrets and variables → Actions`
2. Click "New repository secret" and add:

**Backend Deployment (Render):**
- `RENDER_DEPLOY_HOOK_URL` - Get from [Render Dashboard](https://dashboard.render.com)
  - Service → Settings → Deploy Hook → Copy URL

**Frontend Deployment (Vercel):**
- `VERCEL_TOKEN` - Get from [Vercel Settings](https://vercel.com/account/tokens)
  - Create a new token with full access
- `VERCEL_ORG_ID` - Your Vercel Organization ID
- `VERCEL_PROJECT_ID` - Your SmartTax Assist project ID

📋 [See detailed setup instructions below](#detailed-secrets-setup)

### Step 2: Test the Pipeline

```bash
# Make a small change and commit
git add .
git commit -m "test: verify CI/CD pipeline"
git push origin main
```

Watch it run:
- Go to `GitHub Repo → Actions` tab
- You should see both CI and CD workflows executing
- Check [Render Dashboard](https://dashboard.render.com) and [Vercel Dashboard](https://vercel.com) for deployment status

---

## Pipeline Architecture

### CI Pipeline (`.github/workflows/ci.yml`)

Runs on: **Every push and pull request**

```
┌─────────────────┐
│  Code Pushed    │
└────────┬────────┘
         │
    ┌────▼──────────────────┐
    │  Checkout Code        │
    └────┬──────────────────┘
         │
    ┌────┴──────────────────────────────────┐
    │  Backend Tests                        │
    │  ├─ Install dependencies              │
    │  ├─ Run pytest                        │
    │  └─ Lint Python files                 │
    └────┬──────────────────────────────────┘
         │
    ┌────┴──────────────────────────────────┐
    │  Frontend Tests                       │
    │  ├─ Install dependencies              │
    │  ├─ Run linter (eslint)               │
    │  └─ Build app (check TypeScript)      │
    └────┬──────────────────────────────────┘
         │
    ┌────┴──────────────────────────────────┐
    │  Docker Build                         │
    │  └─ Build images locally              │
    └────┬──────────────────────────────────┘
         │
    ┌────┴──────────────────────────────────┐
    │  Security Scanning (optional)         │
    │  └─ Check for hardcoded secrets       │
    └──────────────────────────────────────┘
```

### CD Pipeline (`.github/workflows/cd.yml`)

Runs on: **Main branch push only** (if CI passes)

```
┌────────────────────────┐
│  Code Pushed to Main   │
└────────┬───────────────┘
         │
         ├─ CI Pipeline Runs First ─┐
         │                           │
    ┌────▼──────────────────────────▼─────┐
    │  All Tests Pass?                     │
    └────┬──────────────────────────────────┘
         │
    ┌────┴────────────────────────────────┐
    │  Deploy Backend to Render           │
    │  └─ POST to Render Deploy Hook      │
    └────┬────────────────────────────────┘
         │
    ┌────┴────────────────────────────────┐
    │  Deploy Frontend to Vercel          │
    │  └─ Use Vercel CLI Token            │
    └────┬────────────────────────────────┘
         │
    ┌────┴────────────────────────────────┐
    │  Health Checks                      │
    │  ├─ Backend /health endpoint        │
    │  └─ Frontend homepage               │
    └────┬────────────────────────────────┘
         │
    ┌────▼────────────────────────────────┐
    │  Deployment Complete                │
    │  ✅ Both services running           │
    └─────────────────────────────────────┘
```

---

## Local Development & Testing

### Run Tests Locally

**Backend:**
```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v
```

**Frontend:**
```bash
cd frontend
npm install
npm test
```

### Run Linters Locally

**Backend:**
```bash
cd backend
python -m pylint app/
```

**Frontend:**
```bash
cd frontend
npm run lint
```

### Build Docker Locally

```bash
docker compose build
docker compose up -d
```

Then visit:
- Backend: http://localhost:8000/docs (Swagger UI)
- Frontend: http://localhost:3000

---

## Health Checks & Monitoring

### Health Endpoints

Once deployed, you can monitor your services:

**Backend Health:**
```bash
curl https://smarttax-backend.onrender.com/health
```

Response:
```json
{
  "status": "ok",
  "service": "SmartTax Assist API",
  "environment": "production"
}
```

**Backend Metrics:**
```bash
curl https://smarttax-backend.onrender.com/metrics
```

Response:
```json
{
  "status": "ok",
  "service": "SmartTax Assist API",
  "environment": "production",
  "uptime_seconds": 3600,
  "total_requests": 1234,
  "error_count": 2,
  "timestamp": "2024-05-09T12:34:56.789012"
}
```

### Set Up Uptime Monitoring (Free)

Use [Uptime Robot](https://uptimerobot.com) to monitor your backend:

1. Sign up (free tier: 50 monitors)
2. Create new monitor:
   - Type: HTTP(s)
   - URL: `https://smarttax-backend.onrender.com/health`
   - Interval: 5 minutes
   - Get alerts via email if service goes down

---

## Detailed Secrets Setup

### Render Deploy Hook

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Select your backend service (`smarttax-backend`)
3. Navigate to **Settings** tab
4. Scroll to **Deploy Hook** section
5. Click "Create Deploy Hook"
6. Copy the URL (looks like: `https://api.render.com/deploy/srv-xxxxx?key=xxxxx`)
7. Go to GitHub Repo → Settings → Secrets → New Secret
   - Name: `RENDER_DEPLOY_HOOK_URL`
   - Value: Paste the URL from step 6

### Vercel Token & IDs

**Get Vercel Token:**
1. Go to [Vercel Account Settings](https://vercel.com/account/tokens)
2. Click "Create" button
3. Give it a name (e.g., "CI/CD Token")
4. Scope: Select your SmartTax Assist project
5. Copy the token
6. Add to GitHub Secrets:
   - Name: `VERCEL_TOKEN`
   - Value: Paste the token

**Get Vercel IDs:**
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your SmartTax Assist project
3. Go to **Settings**
4. Copy these values:
   - **ORG ID**: Settings → General → Organization ID
   - **PROJECT ID**: Settings → General → Project ID
5. Add to GitHub Secrets:
   - Name: `VERCEL_ORG_ID` → Paste Organization ID
   - Name: `VERCEL_PROJECT_ID` → Paste Project ID

---

## Troubleshooting

### CD Pipeline Not Triggering

**Problem:** I pushed to main but CD didn't run

**Solutions:**
1. Check that CI pipeline passed first
   - Go to Actions tab
   - Look for red ❌ or green ✅ on your latest commit
   - If red, fix the failing tests first

2. Verify you pushed to `main` branch
   ```bash
   git branch  # Should show * main
   ```

3. Check GitHub Actions are enabled
   - Repo → Settings → Actions → Enable Actions

### Render Deployment Failed

**Problem:** CD pipeline says "Continue on error" for Render

**Possible Causes:**
- `RENDER_DEPLOY_HOOK_URL` not set in GitHub Secrets
- Deploy hook URL is invalid/expired
- Service doesn't exist on Render

**Fix:**
1. Regenerate deploy hook in Render Dashboard
2. Update GitHub Secret with new URL
3. Re-run workflow: Actions → Latest workflow → Re-run jobs

### Vercel Deployment Failed

**Problem:** Vercel deployment shows error

**Possible Causes:**
- `VERCEL_TOKEN` missing or invalid
- `VERCEL_ORG_ID` or `VERCEL_PROJECT_ID` incorrect
- Build environment variables not set in Vercel

**Fix:**
1. Verify all three Vercel secrets are set correctly
2. Check Vercel Dashboard for build errors
3. Ensure `NEXT_PUBLIC_API_URL` is set to production Render URL

### Tests Failing Locally

```bash
# Backend
cd backend
pip install pytest pytest-cov pytest-asyncio
pytest tests/ -v --tb=short

# Frontend
cd frontend
npm install @testing-library/react @testing-library/jest-dom
npm test -- --no-coverage
```

---

## GitHub Actions Workflow Files

### CI Workflow (`.github/workflows/ci.yml`)

Runs on every push and PR. Key steps:
- Lints Python and TypeScript code
- Runs pytest for backend tests
- Builds frontend Next.js app
- Builds Docker images
- Scans for hardcoded secrets

### CD Workflow (`.github/workflows/cd.yml`)

Runs only on `main` branch push (if CI passes). Key steps:
- Deploys backend to Render via webhook
- Deploys frontend to Vercel via API
- Verifies health endpoints after deployment
- Sends deployment summary

---

## Next Steps

**Phase 2: Security Enhancements** (Recommended)
- [ ] Enable GitHub Dependabot for dependency scanning
- [ ] Enable CodeQL for security scanning
- [ ] Add pre-commit hooks for secrets detection
- [ ] Rotate JWT secrets every 90 days

**Phase 3: Monitoring & Error Tracking**
- [ ] Set up Sentry.io for error tracking
- [ ] Configure error notifications to Slack/Email
- [ ] Create monitoring dashboard

**Phase 4: Testing & Documentation**
- [ ] Write more comprehensive unit tests
- [ ] Add integration tests
- [ ] Set up end-to-end testing
- [ ] Create load testing templates

---

## Support & Resources

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **Render Deployment**: https://render.com/docs/deploy-hooks
- **Vercel CLI**: https://vercel.com/docs/vercel-cli
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Next.js Docs**: https://nextjs.org/docs

