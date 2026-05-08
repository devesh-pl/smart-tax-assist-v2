# 📤 GitHub Push Checklist & Guide

## ✅ Pre-Push Verification

Before pushing code to GitHub, ensure:

### 1. Sensitive Values Are NOT in Code

**Files to check for exposed secrets:**

```bash
# Check for MongoDB URLs in code files
grep -r "mongodb+srv://" . --exclude-dir=node_modules --exclude-dir=.git

# Check for JWT secrets
grep -r "JWT_SECRET" . --exclude-dir=node_modules --exclude-dir=.git --exclude="*.example"

# Check for API keys/passwords
grep -r "password" . --exclude-dir=node_modules --exclude-dir=.git --exclude="*.md"
```

**If found:**
- Move to `.env` file
- Add `*.env` to `.gitignore`
- Use `git rm --cached filename` to remove from git history

### 2. Verify .gitignore is Correct

```bash
git status --ignored
```

Should show as ignored:
- `.env`
- `.env.local`
- `backend/.env`
- `frontend/.env.local`
- `node_modules/`
- `__pycache__/`

### 3. Check for Large Files

```bash
# Find files larger than 50MB
find . -type f -size +50M -not -path "./.git/*"
```

Git LFS is required for files > 100MB.

---

## 🔒 Remove Accidental Commits

If you accidentally committed a `.env` file with secrets:

### Option 1: Remove from Last Commit (Not Yet Pushed)

```bash
# Remove file from staging
git rm --cached backend/.env

# Add to gitignore
echo "backend/.env" >> .gitignore

# Amend the commit
git add .gitignore
git commit --amend --no-edit

# Force push (only if not yet pushed!)
git push origin main --force
```

### Option 2: Remove from Entire History (After Pushed)

**⚠️ DANGEROUS - Use only if secrets are exposed!**

```bash
# Install BFG Repo-Cleaner (or use git-filter-branch)
# https://rtyley.github.io/bfg-repo-cleaner/

# Remove file from all commits
bfg --delete-files backend/.env

# Force push
git push origin main --force

# ⚠️ All contributors must pull with --hard reset
```

**Better option: Rotate credentials immediately!**
- Change MongoDB Atlas password
- Generate new JWT secret
- Invalidate exposed API keys

---

## 📋 Step-by-Step GitHub Push

### Step 1: Create .env Files Locally

```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env with your actual values

# Frontend
cp frontend/.env.local.example frontend/.env.local
# Edit frontend/.env.local with your values
```

### Step 2: Verify Files Are Ignored

```bash
git status
```

Output should NOT show:
```
.env
backend/.env
frontend/.env.local
```

### Step 3: Stage All Changes

```bash
git add .
```

### Step 4: Review Changes Before Commit

```bash
git status
```

### Step 5: Commit

```bash
git commit -m "Initial commit: SmartTax Assist with environment configuration"
```

Or with detailed message:

```bash
git commit -m "feat: Initial deployment setup

- Configure environment variables for frontend and backend
- Update docker-compose.yml to use env vars
- Add .env.example templates for reference
- Update .gitignore to protect sensitive files"
```

### Step 6: Push to GitHub

```bash
# First time push
git remote add origin https://github.com/YOUR_USERNAME/smart-tax-assist-v2.git
git branch -M main
git push -u origin main

# Subsequent pushes
git push origin main
```

### Step 7: Verify on GitHub

Visit: `https://github.com/YOUR_USERNAME/smart-tax-assist-v2`

Verify:
- ✅ All code files present
- ❌ NO `.env` files
- ❌ NO `.env.local` files
- ✅ `.env.example` files present (for reference)

---

## 🔄 Regular Commits & Pushes

After initial setup:

```bash
# Make changes to code
# ... edit files ...

# Check what changed
git status

# Add changes
git add .

# Commit
git commit -m "feature: describe your change"

# Push to GitHub
git push origin main
```

---

## 🚨 Common Mistakes

### ❌ Mistake 1: Pushing .env Files

```bash
# You see this in git status
M .env
M backend/.env
M frontend/.env.local
```

**Solution:**
```bash
# Don't add them
git reset

# Add to .gitignore
echo ".env*" >> .gitignore

# Commit only .gitignore
git add .gitignore
git commit -m "fix: prevent env files from tracking"
git push
```

### ❌ Mistake 2: Hardcoded Secrets in Code

```python
# ❌ BAD - in app/main.py
MONGODB_URL = "mongodb+srv://user:pass@cluster..."
JWT_SECRET = "super-secret-key-123"
```

**Solution:**
```python
# ✅ GOOD - load from env
import os
MONGODB_URL = os.getenv("MONGODB_URL")
JWT_SECRET = os.getenv("JWT_SECRET")
```

### ❌ Mistake 3: Committing node_modules

```bash
# Check if added
git status | grep node_modules

# If yes, remove from tracking
git rm -r --cached node_modules/
echo "node_modules/" >> .gitignore
git commit -m "Remove node_modules from tracking"
```

### ❌ Mistake 4: Large File Commits

**Error:** `"File too large to push (>100MB)"`

**Solution:**
- Use Git LFS for large files
- Remove unnecessary files from repo
- Compress or exclude in .gitignore

---

## 🔐 Private vs Public Repository

### Start Private (Recommended)

1. Create repository as **Private**
2. Push code
3. After verification, make **Public** if needed:
   - GitHub → Repository Settings → Change to Public
   - Only after removing any sensitive data

### Keeping Private

- GitHub: Free accounts can have unlimited private repos
- Use for production/sensitive code
- Share via collaborators or deploy directly

---

## 👥 Adding Collaborators

If working as a team:

1. GitHub → Settings → Collaborators
2. Invite team members
3. Each member gets their own `.env` files locally
4. All `.env` files are git-ignored

---

## 📝 Commit Message Best Practices

Good commit messages:

```
✅ feat: Add OAuth authentication
✅ fix: Resolve CORS issues in production
✅ docs: Update deployment guide
✅ refactor: Optimize database queries
✅ chore: Update dependencies
```

Bad commit messages:

```
❌ fix bug
❌ update
❌ asdf
❌ final version
```

---

## 🚀 After GitHub Push

Your code is now safe in GitHub! Next steps:

1. **Deploy Backend to Render**
   - Render automatically pulls from GitHub
   - See `DEPLOYMENT_GUIDE.md`

2. **Deploy Frontend to Vercel**
   - Vercel automatically pulls from GitHub
   - See `DEPLOYMENT_GUIDE.md`

3. **Future Updates**
   - Make changes locally
   - Commit: `git commit -m "feature: description"`
   - Push: `git push origin main`
   - Both Render and Vercel auto-deploy!

---

## 📚 Useful Git Commands

```bash
# Check commit history
git log --oneline

# See what will be committed
git diff --cached

# Undo last commit (not pushed)
git reset --soft HEAD~1

# Check which files git will ignore
git check-ignore -v *

# Remove file from git history (danger!)
git filter-branch --tree-filter 'rm -f .env' HEAD

# View .env.local without tracking
git update-index --assume-unchanged .env.local

# See all branches
git branch -a
```

---

## ✅ Checklist Before First Push

- [ ] GitHub account created
- [ ] Repository created (Private)
- [ ] Git initialized: `git init`
- [ ] `.env` files created locally (NOT committed)
- [ ] `.gitignore` includes `.env*`
- [ ] No secrets in code files
- [ ] `git add .` executed
- [ ] `git commit` done
- [ ] Remote added: `git remote add origin ...`
- [ ] `git push -u origin main` successful
- [ ] Verified on GitHub (no .env files visible)
- [ ] Render & Vercel connected to GitHub
- [ ] Ready for deployment!

---

**Ready to push! 🚀**
