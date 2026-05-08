# 🔐 Security Checklist & Best Practices

## Before Pushing to GitHub

### Step 1: Verify No Secrets in Code

```bash
# Search for common patterns
grep -r "mongodb\+srv" . --exclude-dir=.git --exclude-dir=node_modules
grep -r "JWT_SECRET\|jwt_secret" . --exclude-dir=.git --exclude-dir=node_modules --exclude="*.md"
grep -r "password\|PASSWORD" . --exclude-dir=.git --exclude-dir=node_modules --exclude="*.md"
grep -r "api_key\|API_KEY\|apiKey" . --exclude-dir=.git --exclude-dir=node_modules --exclude="*.md"
```

**If found:** Move to `.env` files immediately!

### Step 2: Verify .gitignore

Check that these are ignored:

```bash
git check-ignore -v .env .env.local backend/.env frontend/.env.local
```

Output should show all files as ignored.

### Step 3: Remove Accidental Commits

If `.env` was committed before adding to `.gitignore`:

```bash
# Remove from tracking (don't delete the file)
git rm --cached .env backend/.env frontend/.env.local

# Amend last commit
git add .gitignore
git commit --amend --no-edit

# Force push to GitHub (ONLY if not public yet!)
git push origin main --force
```

**⚠️ After pushing:** Assume secrets are compromised! Rotate:
- MongoDB Atlas password
- JWT secret
- Any API keys

---

## Environment Variables Security

### Backend (.env)

**Never expose:**
```env
❌ MONGODB_URL=mongodb+srv://username:password@...
❌ JWT_SECRET=your-actual-secret
```

**Always use:**
```env
✅ MONGODB_URL=<strong-random-url>
✅ JWT_SECRET=<strong-random-key>
✅ ENVIRONMENT=production
```

### Frontend (.env.local)

**Safe to expose (public):**
```env
✅ NEXT_PUBLIC_API_URL=https://api.example.com
✅ NEXT_PUBLIC_ENVIRONMENT=production
```

**Never expose:**
```env
❌ NEXT_PRIVATE_SECRET_KEY=<hidden>
❌ DB_PASSWORD=password123
❌ API_SECRET=secret
```

---

## Deployment Security

### Render (Backend)

1. ✅ Set `ENVIRONMENT=production`
2. ✅ Use strong `JWT_SECRET` (minimum 32 characters)
3. ✅ Use MongoDB Atlas credentials only
4. ✅ Keep service on Free tier (auto-sleeps is acceptable)
5. ⚠️ Monitor logs for errors

**Generate Strong JWT Secret:**

```bash
# Option 1: Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Option 2: OpenSSL
openssl rand -base64 32

# Option 3: Online (⚠️ only for testing)
# https://www.random.org/strings/
```

### Vercel (Frontend)

1. ✅ Set `NEXT_PUBLIC_ENVIRONMENT=production`
2. ✅ Verify `NEXT_PUBLIC_API_URL` points to Render backend
3. ✅ Use production branch only (main)
4. ✅ Monitor build logs

### MongoDB Atlas

1. ✅ Use strong database password (20+ characters)
2. ✅ Enable IP Whitelist (restrict to Render IP)
3. ✅ Enable backups
4. ✅ Use SCRAM authentication (default)
5. ⚠️ Avoid allowing `0.0.0.0/0` in production (only for testing)

---

## API Security

### Authentication

✅ **Implemented:**
- Password hashing with bcrypt (rounds: 12)
- JWT tokens with expiration (24 hours)
- Token-based auth on protected routes

### CORS

✅ **Secured:**
```python
# Development
allow_origins=["http://localhost:3000"]

# Production
allow_origins=["https://smart-tax-assist-v2.vercel.app"]
```

### HTTPS

✅ **Automatic:**
- Vercel: HTTPS required by default
- Render: HTTPS required by default

### Rate Limiting

⚠️ **Not implemented** - Consider adding:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/data")
@limiter.limit("100/minute")
async def get_data():
    pass
```

### Input Validation

✅ **Implemented via Pydantic:**
```python
class ExpenseCreate(BaseModel):
    amount: float
    date: Optional[str] = None
```

---

## Database Security

### MongoDB

✅ **Configured:**
- SCRAM authentication
- User permissions per database
- IP whitelist (configurable)

### Backup Strategy

1. **Automated Backups:**
   - MongoDB Atlas: 7-day retention (free)
   - Or 35 days (paid)

2. **Manual Backup:**
```bash
mongodump --uri "mongodb+srv://username:password@cluster..."
```

3. **Restore:**
```bash
mongorestore dump/
```

---

## GitHub Repository Security

### Repository Settings

1. **Private Repository** (recommended for initial development)
   - GitHub → Settings → General → Change to Private

2. **Branch Protection** (for team projects)
   - Settings → Branches → Add rule for `main`
   - Require pull request reviews before merging
   - Dismiss stale reviews

3. **Secrets Management**
   - Don't use GitHub Secrets for `.env` files
   - Use Render/Vercel environment variables instead

### Collaborators Access

- Limit who can access the repository
- Review who has push access
- Rotate access when team members leave

---

## Code Security

### Dependencies

Check for vulnerabilities:

```bash
# Backend
cd backend
pip check

# Frontend
cd frontend
npm audit
npm audit fix  # Only fixes if safe
```

### Regular Updates

```bash
# Backend
pip list --outdated
pip install --upgrade package-name

# Frontend
npm outdated
npm update
```

### OWASP Top 10 Checklist

- ✅ Broken Access Control: JWT tokens verify identity
- ✅ Cryptographic Failures: Passwords hashed, HTTPS enforced
- ⚠️ Injection: Use parameterized queries (MongoDB does this)
- ⚠️ Insecure Design: Follow secure coding practices
- ⚠️ Security Misconfiguration: Review all configs
- ⚠️ Vulnerable Components: Keep dependencies updated

---

## Logging & Monitoring

### What to Log

✅ **Log these:**
- Authentication attempts
- API errors (status codes)
- Database operations (general)
- Deployment events

❌ **Never log:**
- Passwords
- JWT tokens
- Sensitive user data
- API keys/secrets

### Monitoring Tools

**Render:**
- Logs tab shows real-time output
- Email alerts for errors

**Vercel:**
- Analytics dashboard
- Build logs
- Runtime logs (tailing)

**MongoDB:**
- Atlas → Monitoring
- Query profiler
- Connection stats

---

## Incident Response

### If Secrets Are Exposed

1. **Immediately rotate:**
```bash
# MongoDB Atlas password
# JWT secret (update in Render env vars)
# Any API keys
```

2. **Audit access logs:**
   - MongoDB Atlas → Activity
   - Render → Logs

3. **Force re-authenticate:**
   - Update JWT_EXPIRATION_HOURS to 1 (temporary)
   - Deploy
   - Users re-login

4. **Investigate:**
   - Check git history
   - Review who had access
   - Implement additional controls

### If Database Is Compromised

1. **Backup immediately:**
```bash
mongodump --uri "mongodb+srv://..."
```

2. **Change password:**
   - MongoDB Atlas → Database Access

3. **Review audit logs:**
   - Who accessed what data
   - What queries were run

4. **Consider IP whitelist:**
   - Restrict to only Render IP

---

## Production Checklist

Before marking as Production:

- [ ] All secrets in environment variables
- [ ] No hardcoded credentials in code
- [ ] `.env*` files in `.gitignore`
- [ ] CORS restricted to known domains
- [ ] HTTPS enforced (automatic)
- [ ] Rate limiting considered
- [ ] Input validation implemented
- [ ] Error messages don't leak info
- [ ] Logs don't contain sensitive data
- [ ] Backups configured
- [ ] Monitoring in place
- [ ] Team knows security policies
- [ ] Dependencies updated
- [ ] Documentation complete

---

## Security Headers

### Frontend (Next.js)

Add to `next.config.js`:

```javascript
async headers() {
  return [
    {
      source: "/(.*)",
      headers: [
        {
          key: "X-Content-Type-Options",
          value: "nosniff"
        },
        {
          key: "X-Frame-Options",
          value: "DENY"
        },
        {
          key: "X-XSS-Protection",
          value: "1; mode=block"
        }
      ]
    }
  ]
}
```

### Backend (FastAPI)

Add to `app/main.py`:

```python
from starlette.middleware.base import BaseHTTPMiddleware

app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=add_security_headers
)

async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response
```

---

## Regular Security Audits

Schedule:
- **Monthly:** Dependency updates (`npm audit`, `pip check`)
- **Quarterly:** Code review for security issues
- **Annually:** Full security audit

---

## Resources

- 🔐 OWASP Top 10: https://owasp.org/www-project-top-ten/
- 🔐 NIST Guidelines: https://csrc.nist.gov/
- 🔐 GitHub Security: https://docs.github.com/en/code-security
- 🔐 MongoDB Security: https://www.mongodb.com/docs/manual/security/

---

**Your application is now secured! 🛡️**

Remember: Security is not a feature, it's a continuous process.
