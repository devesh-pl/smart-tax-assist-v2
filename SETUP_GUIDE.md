# SmartTax Assist - Authentication & Database Setup Guide

## ✅ Implementation Status: COMPLETE

All authentication, database integration, and user isolation features have been successfully implemented.

---

## 📋 Next Steps to Run the Application

### Step 1: Prepare MongoDB

You need a MongoDB instance. Choose one option:

**Option A: MongoDB Atlas (Cloud - Recommended)**
1. Go to https://cloud.mongodb.com
2. Create a free account
3. Create a new cluster
4. Get your connection string in format: `mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority`
5. Copy the connection string

**Option B: Local MongoDB**
1. Install MongoDB locally: https://docs.mongodb.com/manual/installation/
2. Start MongoDB service: `mongod`
3. Connection string: `mongodb://localhost:27017/smart_tax_assist`

### Step 2: Configure Backend Environment

1. Navigate to `backend/` directory
2. Open `.env` file (already created, currently empty)
3. Fill in your MongoDB credentials:

```bash
# backend/.env
MONGODB_URL=mongodb+srv://your-username:your-password@your-cluster.mongodb.net/?retryWrites=true&w=majority

# Generate a random JWT secret (run in terminal):
# python -c "import secrets; print(secrets.token_urlsafe(32))"
JWT_SECRET=<paste-generated-secret-here>

JWT_EXPIRATION_HOURS=24
JWT_ALGORITHM=HS256
```

**Example .env file:**
```
MONGODB_URL=mongodb+srv://admin:MyPassword123@smarttax.abcd1234.mongodb.net/?retryWrites=true&w=majority
JWT_SECRET=K8vQ2pX_-R5tH9wJL3mN6yU7sK0aB1cD2eF4gH5i
JWT_EXPIRATION_HOURS=24
JWT_ALGORITHM=HS256
```

### Step 3: Install Backend Dependencies

```bash
cd backend/
pip install -r requirements.txt
```

If you're using Python 3 specifically:
```bash
pip3 install -r requirements.txt
```

### Step 4: Run Backend Server

```bash
cd backend/
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
✓ MongoDB connection established
✓ Application startup complete
Uvicorn running on http://0.0.0.0:8000
```

### Step 5: Configure Frontend Environment (if needed)

Check `frontend/.env.local` exists with:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

If not present, create it with the above content.

### Step 6: Install & Run Frontend

```bash
cd frontend/
npm install
npm run dev
```

Frontend will be available at `http://localhost:3000`

---

## 🧪 Testing the Implementation

### 1. Test Signup
1. Open http://localhost:3000
2. You'll be redirected to login page (no user logged in yet)
3. Click "Sign up"
4. Fill in email, full name, password (min 6 chars)
5. Password must match confirmation
6. Click "Sign up"
7. You should be redirected to Dashboard if successful

**Expected in MongoDB `users` collection:**
```json
{
  "_id": ObjectId("..."),
  "email": "user@example.com",
  "full_name": "John Doe",
  "password_hash": "$2b$12$...",  // bcrypt hash, never plaintext
  "created_at": ISODate("2024-01-15T10:30:00Z"),
  "updated_at": ISODate("2024-01-15T10:30:00Z")
}
```

### 2. Test Login
1. Logout (click Logout button in sidebar)
2. You'll be redirected to login page
3. Enter your email and password
4. Click "Sign in"
5. Should redirect to Dashboard

### 3. Test User Isolation
1. User A uploads a bill
2. User A can see the bill in `/expenses`
3. Logout (User A's token deleted from localStorage)
4. Login as User B (create new account)
5. User B's `/expenses` is empty (different MongoDB `user_id`)
6. Login back as User A → bill is still there

### 4. Test Protected Routes
1. Logout
2. Try accessing `http://localhost:3000/expenses` directly
3. You should be redirected to login page

### 5. Test API Endpoints with Curl

```bash
# Signup
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123","full_name":"Test User"}'

# Response:
# {
#   "access_token": "eyJhbGc...",
#   "token_type": "bearer",
#   "user": {"id": "...", "email": "test@example.com", "full_name": "Test User"}
# }

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123"}'

# Get current user (protected)
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Get expenses (protected, user-isolated)
curl -X GET http://localhost:8000/expenses \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📊 Database Schema Created

### Collections in MongoDB

**1. `users`**
```json
{
  "_id": ObjectId,
  "email": String (unique, indexed),
  "full_name": String,
  "password_hash": String (bcrypt),
  "created_at": DateTime,
  "updated_at": DateTime
}
```
**Indexes:** `email` (unique)

**2. `expenses`**
```json
{
  "_id": ObjectId,
  "user_id": ObjectId (ref to users._id),
  "bill_name": String,
  "vendor": String,
  "category": String,
  "expense_type": String,
  "amount": Number,
  "gst": Number,
  "date": String,
  "created_at": DateTime,
  "updated_at": DateTime
}
```
**Indexes:** `user_id` (for filtering), `date` (for sorting)

**3. `categories`**
```json
{
  "_id": ObjectId,
  "user_id": ObjectId (ref to users._id),
  "name": String,
  "created_at": DateTime
}
```
**Indexes:** `user_id` (for filtering)

---

## 🔐 Security Features Implemented

1. **Password Hashing:** Bcrypt (12 rounds) - passwords never stored plaintext
2. **JWT Tokens:** HS256 algorithm, 24-hour expiration
3. **User Isolation:** All data filtered by `user_id` at database level
4. **CORS:** Only localhost:3000 and 127.0.0.1:3000 allowed
5. **Protected Routes:** Frontend routes require valid JWT token
6. **401 Handling:** Auto-logout if token invalid/expired

---

## 📝 API Endpoints

### Authentication (Public)
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Get JWT token
- `POST /auth/logout` - Invalidate token (token-based, frontend deletes)

### Authentication (Protected)
- `GET /auth/me` - Get current user profile

### Expenses (Protected - User Isolated)
- `GET /expenses` - Get user's expenses with filters
- `GET /expenses/summary` - Get user's expense summary
- `POST /upload-bill` - Upload and OCR bill
- `PUT /expenses/{id}` - Update expense
- `DELETE /expenses/{id}` - Delete expense

### Categories (Protected - User Isolated)
- `GET /categories` - Get user's categories
- `POST /categories` - Add category
- `PUT /categories/{name}` - Rename category
- `DELETE /categories/{name}` - Delete category

### Export (Protected - User Isolated)
- `GET /export-excel` - Download Excel report

---

## 🚀 Docker Deployment (Optional)

If using Docker, update `backend/.env` in docker-compose.yml:

```yaml
services:
  backend:
    environment:
      MONGODB_URL: ${MONGODB_URL}
      JWT_SECRET: ${JWT_SECRET}
    # ... rest of config
```

Run with:
```bash
docker-compose up --build
```

---

## ❓ Troubleshooting

### "Failed to connect to MongoDB"
- Check MONGODB_URL is correct
- Ensure MongoDB service is running
- For Atlas: verify IP is whitelisted (or use 0.0.0.0/0)
- Network connection issue: check firewall

### "Invalid token" errors
- Token may have expired (24-hour limit)
- Logout and login again
- Check browser localStorage has token

### "User not found"
- User may have been deleted from database
- Signup again with new credentials

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check NEXT_PUBLIC_API_URL in frontend/.env.local
- CORS should allow localhost:3000

---

## 🎯 Key Files & Their Roles

**Backend**
- `app/main.py` - FastAPI app setup, DB init, routes
- `app/services/auth_service.py` - Core auth logic
- `app/utils/db.py` - MongoDB connection
- `app/routes/auth.py` - Signup/login endpoints
- `.env` - Your secret credentials (DON'T COMMIT)

**Frontend**
- `context/AuthContext.tsx` - Global auth state
- `hooks/useAuth.ts` - Auth hook for components
- `components/ProtectedRoute.tsx` - Route protection
- `lib/api.ts` - API client with JWT handling
- `app/auth/login/page.tsx` - Login UI
- `app/auth/signup/page.tsx` - Signup UI

---

## ✨ What's New vs Original

| Feature | Before | After |
|---------|--------|-------|
| Storage | In-memory (lost on restart) | MongoDB (persistent) |
| Users | Single user | Multi-user with isolation |
| Authentication | None | JWT-based signup/login |
| Passwords | N/A | Bcrypt hashed |
| Data Isolation | All data visible to all | Each user sees only their data |
| Login Page | None | Full signup/login UI |
| Protected Routes | None | All dashboard routes protected |
| Logout | None | Logout button in sidebar |

---

## 📞 Support

If you encounter issues:
1. Check error logs in terminal (backend & frontend)
2. Verify MongoDB connection string
3. Ensure JWT_SECRET is set and strong
4. Check firewall/network settings
5. Look at browser console (F12) for frontend errors

---

**Version:** 1.0.0 with Authentication & MongoDB  
**Last Updated:** May 6, 2026
