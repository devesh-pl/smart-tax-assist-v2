# 🚀 Quick Start Checklist

Follow these steps in order to get SmartTax Assist with authentication running:

## ✅ Prerequisites (Do First)

- [ ] **Get MongoDB Connection String**
  - Option A: Create free cluster at https://cloud.mongodb.com
  - Option B: Have local MongoDB installed & running
  - Connection string format: `mongodb+srv://user:pass@cluster.mongodb.net/...` or `mongodb://localhost:27017`

- [ ] **Generate JWT Secret**
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
  Copy the output (looks like: `K8vQ2pX_-R5tH9wJL3mN6yU7sK0aB1cD2eF4gH5i`)

---

## 🔧 Backend Setup

1. [ ] **Edit `backend/.env`**
   ```
   MONGODB_URL=<paste-your-mongodb-url-here>
   JWT_SECRET=<paste-your-generated-secret-here>
   JWT_EXPIRATION_HOURS=24
   JWT_ALGORITHM=HS256
   ```

2. [ ] **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. [ ] **Start backend server**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   Should see:
   ```
   ✓ MongoDB connection established
   Uvicorn running on http://0.0.0.0:8000
   ```

---

## 🎨 Frontend Setup

1. [ ] **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. [ ] **Verify `.env.local`** (should already exist)
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. [ ] **Start frontend server**
   ```bash
   cd frontend
   npm run dev
   ```
   
   Should see:
   ```
   ▲ Next.js
   ▲ Ready in 1234ms
   ▲ Local: http://localhost:3000
   ```

---

## 🧪 Test Everything Works

1. [ ] Open http://localhost:3000 in browser
2. [ ] You're redirected to `/auth/login` (no user logged in)
3. [ ] Click "Sign up"
4. [ ] Create account with:
   - Email: `test@example.com`
   - Full Name: `Test User`
   - Password: `Password123`
5. [ ] You should see Dashboard with empty expenses
6. [ ] Click "Logout" button in sidebar
7. [ ] You're back at login page
8. [ ] Login with same credentials
9. [ ] Dashboard appears again

---

## ✨ You're Done!

The system is now running with:
- ✅ User registration (signup)
- ✅ User authentication (login)
- ✅ JWT token-based security
- ✅ User data isolation (each user sees only their data)
- ✅ Protected routes (can't access dashboard without login)
- ✅ Persistent database (MongoDB)
- ✅ Password hashing (bcrypt)

---

## 🆘 Common Issues

| Issue | Solution |
|-------|----------|
| "Failed to connect to MongoDB" | Check MONGODB_URL in `.env` is correct |
| Backend won't start | Ensure port 8000 is free: `lsof -i :8000` |
| Frontend won't start | Ensure port 3000 is free: `lsof -i :3000` |
| Can't login after signup | Check browser console (F12) for errors |
| Expenses disappear after logout | This is expected - each user sees only their data |
| "Invalid token" error | Token expires after 24 hours, logout and login again |

---

**Next Steps After Setup:**
- [ ] Test uploading bills
- [ ] Test category management
- [ ] Test expense filtering
- [ ] Test Excel export
- [ ] Create multiple test users to verify data isolation

---

**Questions?** Refer to [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed information.
