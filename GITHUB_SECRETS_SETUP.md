# 🔐 GitHub Secrets Setup - Quick Reference

## What Are GitHub Secrets?

GitHub Secrets are encrypted environment variables that hold sensitive information (API tokens, webhooks, etc.). They're used by CI/CD workflows without exposing them in logs or code.

---

## Required Secrets

Add these to your GitHub repository to enable auto-deployment:

### Location
`GitHub Repo → Settings → Secrets and variables → Actions → New repository secret`

### 3 Required Secrets

| Secret Name | Value | Where to Get | Required For |
|-------------|-------|-------------|---|
| `RENDER_DEPLOY_HOOK_URL` | Webhook URL from Render | [Render Dashboard](#render-deploy-hook) | Backend auto-deploy |
| `VERCEL_TOKEN` | API token from Vercel | [Vercel Settings](#vercel-token) | Frontend auto-deploy |
| `VERCEL_ORG_ID` | Your Vercel Organization ID | [Vercel Dashboard](#vercel-ids) | Frontend auto-deploy |
| `VERCEL_PROJECT_ID` | Your SmartTax project ID | [Vercel Dashboard](#vercel-ids) | Frontend auto-deploy |

---

## Step-by-Step Setup

### 1️⃣ Render Deploy Hook

**Purpose:** Tells Render to deploy backend when GitHub Actions triggers it

**Steps:**

1. Open [Render Dashboard](https://dashboard.render.com)
2. Click on your backend service: **smarttax-backend**
3. Go to **Settings** tab
4. Scroll down to **Deploy Hook** section
5. Click **Create Deploy Hook**
6. Copy the full URL (Example: `https://api.render.com/deploy/srv-xxxxxxxxxxxxx?key=xxxxxxxxxxxxx`)
7. Go to GitHub:
   - Repo → Settings → Secrets and variables → Actions
   - Click **New repository secret**
   - Name: `RENDER_DEPLOY_HOOK_URL`
   - Value: Paste the copied URL
   - Click **Add secret**

✅ **Done!** Backend will now auto-deploy on GitHub push.

---

### 2️⃣ Vercel Token

**Purpose:** Authenticates GitHub Actions to deploy frontend to Vercel

**Steps:**

1. Go to [Vercel Account Settings → Tokens](https://vercel.com/account/tokens)
2. Click **Create** button
3. Fill in:
   - **Token Name:** `SmartTax CI/CD` (or any name)
   - **Scope:** Select your SmartTax Assist project
   - **Expiration:** Choose based on security preference
4. Click **Create Token**
5. **⚠️ Copy immediately** (won't be shown again)
6. Go to GitHub:
   - Repo → Settings → Secrets and variables → Actions
   - Click **New repository secret**
   - Name: `VERCEL_TOKEN`
   - Value: Paste the token
   - Click **Add secret**

✅ **Done!** Now add the IDs (see next step).

---

### 3️⃣ Vercel Organization ID & Project ID

**Purpose:** Identifies which Vercel project to deploy to

**Steps:**

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your **SmartTax Assist** project
3. Go to **Settings** tab (top right)
4. Under **General**, find:
   - **Organization ID** (e.g., `team_xxxxx` or `usr_xxxxx`)
   - **Project ID** (e.g., `prj_xxxxx`)
5. Copy each one
6. Go to GitHub:
   - Repo → Settings → Secrets and variables → Actions
   - Add first secret:
     - Name: `VERCEL_ORG_ID`
     - Value: Paste Organization ID
     - Click **Add secret**
   - Add second secret:
     - Name: `VERCEL_PROJECT_ID`
     - Value: Paste Project ID
     - Click **Add secret**

✅ **Done!** Frontend will now auto-deploy on GitHub push.

---

## Verify Secrets Are Set

Go to: `GitHub Repo → Settings → Secrets and variables → Actions`

You should see all 4 secrets listed (values hidden):
```
RENDER_DEPLOY_HOOK_URL    ●●●●●●●●●
VERCEL_TOKEN              ●●●●●●●●●
VERCEL_ORG_ID             ●●●●●●●●●
VERCEL_PROJECT_ID         ●●●●●●●●●
```

---

## Test the Setup

1. Make a small change to your code:
   ```bash
   echo "# Testing DevOps" >> README.md
   git add README.md
   git commit -m "test: verify CD pipeline setup"
   git push origin main
   ```

2. Watch it deploy:
   - Go to GitHub Repo → **Actions** tab
   - Click the latest workflow
   - You should see:
     - ✅ CI Pipeline: Lint, Test, Build (5-10 min)
     - ✅ Deploy Backend: Renders to Render (1-2 min)
     - ✅ Deploy Frontend: Deploy to Vercel (2-5 min)

3. Verify services are live:
   ```bash
   # Backend
   curl https://smarttax-backend.onrender.com/health
   
   # Frontend
   curl https://smart-tax-assist-v2.vercel.app/
   ```

---

## Troubleshooting

### "Secret not found" Error in Workflow

**Problem:** Workflow fails because it can't find the secret

**Solution:**
1. Check the secret **Name** exactly matches the workflow file
2. In `.github/workflows/cd.yml`, these are used:
   - `${{ secrets.RENDER_DEPLOY_HOOK_URL }}`
   - `${{ secrets.VERCEL_TOKEN }}`
   - `${{ secrets.VERCEL_ORG_ID }}`
   - `${{ secrets.VERCEL_PROJECT_ID }}`

3. Verify secrets in GitHub are spelled identically (case-sensitive)

### "Invalid Token" Error

**Problem:** Vercel deployment fails with invalid token

**Solution:**
1. Go back to [Vercel Tokens](https://vercel.com/account/tokens)
2. Delete the old token
3. Create a new one following Step 2️⃣ above
4. Update GitHub Secret with new token
5. Re-run the workflow

### "Deploy Hook URL Invalid"

**Problem:** Render deployment says webhook URL is invalid

**Solution:**
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Open smarttax-backend service
3. Go to Settings → Deploy Hook
4. Delete old hook, create new one
5. Copy the full URL
6. Update GitHub Secret `RENDER_DEPLOY_HOOK_URL`
7. Re-run the workflow

---

## Security Best Practices

✅ **Do:**
- Rotate tokens every 3-6 months
- Use organization/project-specific tokens (not personal)
- Set token expiration dates
- Review GitHub secret access in audit logs

❌ **Don't:**
- Commit secrets to code or `.env` files
- Share token values via Slack/email
- Use the same token across multiple projects
- Leave tokens without expiration dates

---

## Next Phase: Auto-Rotation

When you're ready for advanced security:
- [ ] Set up GitHub secret auto-rotation (Enterprise)
- [ ] Use GitHub's OIDC for Vercel (no tokens needed)
- [ ] Implement secret scanning with TruffleHog

---

## Questions?

- Check workflow logs: GitHub Repo → Actions → Click workflow → View logs
- Render support: https://support.render.com
- Vercel support: https://vercel.com/support
- GitHub Actions docs: https://docs.github.com/en/actions

