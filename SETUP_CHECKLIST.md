# SmartTax Assist v1.1 - Setup Checklist

## Pre-Setup Requirements ✓

- [ ] MongoDB account created (Atlas or local instance ready)
- [ ] MongoDB connection string copied to clipboard
- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] Tesseract and Poppler installed (for OCR)

---

## Step 1: Configure Backend Environment

- [ ] Open `backend/.env` in text editor
- [ ] Add MongoDB URL:
  ```
  MONGODB_URL=your_connection_string_here
  ```
- [ ] Generate JWT secret with:
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
- [ ] Add JWT secret:
  ```
  JWT_SECRET=generated_secret_here
  ```
- [ ] Add:
  ```
  JWT_EXPIRATION_HOURS=24
  JWT_ALGORITHM=HS256
  ```
- [ ] Save and close `.env`

---

## Step 2: Install Backend Dependencies

```bash
cd backend
python -m venv venv
```

Activate virtual environment:
- [ ] **macOS/Linux:** `source venv/bin/activate`
- [ ] **Windows:** `venv\Scripts\activate`

Install packages:
```bash
pip install -r requirements.txt
```

- [ ] Verify no errors during installation
- [ ] Check that 4 packages added: pymongo, bcrypt, PyJWT, python-dotenv

---

## Step 3: Install Frontend Dependencies

```bash
cd frontend
npm install
```

- [ ] Verify `node_modules/` created
- [ ] No errors during installation
- [ ] Verify `.env.local` contains: `NEXT_PUBLIC_API_URL=http://localhost:8000`

---

## Step 4: Start Backend Server

In terminal, from `backend/` directory:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

- [ ] See message: "✓ MongoDB connection established"
- [ ] See message: "Uvicorn running on http://0.0.0.0:8000"
- [ ] See message: "Application startup complete"
- [ ] No errors in console

**Leave this terminal running.**

---

## Step 5: Start Frontend Server

In **new terminal**, from `frontend/` directory:

```bash
npm run dev
```

- [ ] See message: "Ready in XXXX ms"
- [ ] See message: "Local: http://localhost:3000"
- [ ] No errors in console

**Leave this terminal running.**

---

## Step 6: Test Authentication

### Test Signup

- [ ] Open http://localhost:3000 in browser
- [ ] Should be redirected to `/auth/login` (not logged in)
- [ ] Click "Sign up"
- [ ] Enter:
  - Email: `test1@example.com`
  - Full Name: `Test User 1`
  - Password: `Password123`
  - Confirm: `Password123`
- [ ] Click "Sign up" button
- [ ] Should redirect to `/expenses` (dashboard)
- [ ] Sidebar should show "Test User 1" and "test1@example.com"

### Test Logout

- [ ] Click "Logout" button in sidebar
- [ ] Should redirect to `/auth/login`
- [ ] Sidebar should disappear

### Test Login

- [ ] Click "Sign up" link
- [ ] Actually click "Login" link (go back to login)
- [ ] Enter:
  - Email: `test1@example.com`
  - Password: `Password123`
- [ ] Click "Login" button
- [ ] Should redirect to `/expenses`
- [ ] Sidebar should show your name again

### Test Multi-User Isolation

- [ ] Log out (click Logout button)
- [ ] Sign up as second user:
  - Email: `test2@example.com`
  - Full Name: `Test User 2`
  - Password: `Password456`
- [ ] Should be on dashboard as "Test User 2"
- [ ] Try to upload a bill or create an expense (optional)
- [ ] Logout and login as User 1
- [ ] Verify User 2's expenses are NOT visible
- [ ] Verify you see the same data as before

---

## Step 7: Test API Directly (Optional)

Test endpoints with curl:

### Signup
```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"email":"api@example.com","password":"Pass123","full_name":"API Test"}'
```

### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"api@example.com","password":"Pass123"}'
```

### Get Current User (replace TOKEN with actual token)
```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer TOKEN"
```

### Check Expenses (should be empty for new user)
```bash
curl -X GET "http://localhost:8000/expenses" \
  -H "Authorization: Bearer TOKEN"
```

---

## Step 8: Verify Database (Optional)

Check MongoDB to see data:

### MongoDB Atlas
1. Log into https://cloud.mongodb.com
2. Click your cluster
3. Click "Collections" tab
4. Browse `smart_tax_assist` database
5. Verify:
   - [ ] `users` collection has your test users
   - [ ] Passwords are hashed (start with $2b$12$)
   - [ ] `expenses` collection (may be empty)
   - [ ] `categories` collection (may be empty)

### Local MongoDB
```bash
mongosh  # or mongo
use smart_tax_assist
db.users.find()      # Should see hashed passwords
db.expenses.find()   # May be empty
db.categories.find() # May be empty
```

---

## Troubleshooting

### Backend won't start

**Error: "Port 8000 already in use"**
- [ ] Close other applications using port 8000
- [ ] Or use different port: `--port 9000`

**Error: "MongoDB connection failed"**
- [ ] Verify `MONGODB_URL` in `backend/.env` is correct
- [ ] If using Atlas: Check IP whitelist (should be 0.0.0.0/0 for development)
- [ ] If using local: Verify `mongod` is running

**Error: "ModuleNotFoundError: No module named X"**
- [ ] Verify virtual environment is activated
- [ ] Run: `pip install -r requirements.txt`

### Frontend won't start

**Error: "Port 3000 already in use"**
- [ ] Use different port: `npm run dev -- -p 3001`

**Error: "Cannot find module"**
- [ ] Delete `node_modules/` folder
- [ ] Run: `npm install`

### Can't login

**Error: "Invalid credentials"**
- [ ] Verify email and password are correct
- [ ] Check if user exists in MongoDB

**Error: "Token not valid"**
- [ ] Log out and log back in
- [ ] Clear browser cache (Ctrl+Shift+Delete)

### Expenses not showing

- [ ] Verify you're logged in (check sidebar)
- [ ] Try uploading a bill first
- [ ] Check browser console (F12) for errors

### Can't see other user's data

- [ ] This is correct! Data isolation is working
- [ ] Each user should only see their own expenses

---

## Success Indicators

When everything is working:

✅ Can sign up with new email  
✅ Can log in with email/password  
✅ See your name in sidebar when logged in  
✅ Get redirected to login when accessing dashboard without token  
✅ Can log out  
✅ Can log back in with same credentials  
✅ Two different users see different expense lists  
✅ Can upload bills and see expenses  
✅ Can export Excel with your data  
✅ Sidebar shows logged-in user's name  

---

## Next Steps After Setup

1. **Read Documentation:**
   - [ ] Review `README.md` for feature overview
   - [ ] Check `IMPLEMENTATION_SUMMARY.md` for architecture

2. **Explore Code:**
   - [ ] Look at `backend/app/services/auth_service.py` (how auth works)
   - [ ] Check `frontend/src/context/AuthContext.tsx` (state management)
   - [ ] Review `backend/app/routes/auth.py` (API endpoints)

3. **Customization:**
   - [ ] Change JWT expiration time in `.env`
   - [ ] Add more validation to signup form
   - [ ] Add email verification (optional feature)
   - [ ] Change password hashing rounds (in auth_service.py)

4. **Deployment:**
   - [ ] Set up production MongoDB instance
   - [ ] Update `.env` with production credentials
   - [ ] Configure CORS for your domain
   - [ ] Use production build: `npm run build`

---

## Support

If you get stuck:

1. **Check the docs:**
   - [ ] Read [SETUP_GUIDE.md](SETUP_GUIDE.md) troubleshooting
   - [ ] Check [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) architecture
   - [ ] Review [DATABASE_DESIGN.md](DATABASE_DESIGN.md) for schema

2. **Check the code:**
   - [ ] Look at error message in terminal
   - [ ] Check browser console (F12 → Console tab)
   - [ ] Review recent changes in related files

3. **Common issues:**
   - [ ] MongoDB not running → Start it
   - [ ] Wrong connection string → Check .env
   - [ ] Dependency missing → Run pip/npm install
   - [ ] Port in use → Change port number

---

## Checklist Summary

**Setup (Est. 20 min):**
- [ ] Step 1: Configure .env ✓
- [ ] Step 2: Install backend ✓
- [ ] Step 3: Install frontend ✓
- [ ] Step 4: Start backend ✓
- [ ] Step 5: Start frontend ✓

**Testing (Est. 10 min):**
- [ ] Step 6: Auth flow ✓
- [ ] Step 7: API testing ✓
- [ ] Step 8: Database check ✓

**Ready to use!**

---

**Date:** May 6, 2026  
**Version:** 1.1.0 (Authentication + MongoDB)  
**Status:** Ready to setup

Start with Step 1! 🚀
