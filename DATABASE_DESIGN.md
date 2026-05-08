# MongoDB Database Design for SmartTax Assist

## Database Overview

**Database Name:** `smart_tax_assist`  
**Database Type:** MongoDB (NoSQL, Document-Based)  
**Storage:** Persistent (Cloud or Local)

---

## Collections & Schemas

### 1. **`users` Collection**

Stores user account information.

**Schema:**
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "email": "john.doe@example.com",
  "full_name": "John Doe",
  "password_hash": "$2b$12$R9h7cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ee7bHECLMvh1T1ZW",
  "created_at": ISODate("2024-01-15T10:30:45.000Z"),
  "updated_at": ISODate("2024-01-15T10:30:45.000Z")
}
```

**Field Descriptions:**
| Field | Type | Description |
|-------|------|-------------|
| `_id` | ObjectId | Unique MongoDB ID (auto-generated) |
| `email` | String | User's email (unique, used for login) |
| `full_name` | String | User's display name |
| `password_hash` | String | Bcrypt-hashed password (never plaintext) |
| `created_at` | DateTime | Account creation timestamp |
| `updated_at` | DateTime | Last account update timestamp |

**Indexes:**
```javascript
db.users.createIndex({ "email": 1 }, { unique: true })
```

**Sample Insert:**
```javascript
db.users.insertOne({
  "email": "john.doe@example.com",
  "full_name": "John Doe",
  "password_hash": "$2b$12$...",  // bcrypt(password)
  "created_at": new Date(),
  "updated_at": new Date()
})
```

---

### 2. **`expenses` Collection**

Stores expense records (bills) for each user.

**Schema:**
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439012"),
  "user_id": ObjectId("507f1f77bcf86cd799439011"),
  "bill_name": "Starbucks Receipt",
  "vendor": "Starbucks Coffee",
  "category": "Food",
  "expense_type": "Personal",
  "amount": 15.50,
  "gst": 1.55,
  "date": "2024-01-15",
  "created_at": ISODate("2024-01-15T10:35:20.000Z"),
  "updated_at": ISODate("2024-01-15T10:35:20.000Z")
}
```

**Field Descriptions:**
| Field | Type | Description |
|-------|------|-------------|
| `_id` | ObjectId | Unique expense ID |
| `user_id` | ObjectId | References `users._id` (ownership) |
| `bill_name` | String | Name/title of the bill |
| `vendor` | String | Vendor/business name (extracted via OCR) |
| `category` | String | Expense category (Food, Travel, etc.) |
| `expense_type` | String | "Personal" or "Business" |
| `amount` | Number | Expense amount in currency |
| `gst` | Number | GST/tax amount |
| `date` | String | Bill date (YYYY-MM-DD format) |
| `created_at` | DateTime | When expense was added |
| `updated_at` | DateTime | Last modification timestamp |

**Indexes:**
```javascript
db.expenses.createIndex({ "user_id": 1 })  // Query by user
db.expenses.createIndex({ "date": 1 })      // Sort by date
db.expenses.createIndex({ "user_id": 1, "date": 1 })  // Composite
```

**Sample Insert:**
```javascript
db.expenses.insertOne({
  "user_id": ObjectId("507f1f77bcf86cd799439011"),
  "bill_name": "Starbucks Receipt",
  "vendor": "Starbucks Coffee",
  "category": "Food",
  "expense_type": "Personal",
  "amount": 15.50,
  "gst": 1.55,
  "date": "2024-01-15",
  "created_at": new Date(),
  "updated_at": new Date()
})
```

**Typical Query (Fetch user's expenses):**
```javascript
db.expenses.find({ 
  "user_id": ObjectId("507f1f77bcf86cd799439011"),
  "date": { "$gte": "2024-01-01", "$lte": "2024-01-31" }
})
```

---

### 3. **`categories` Collection**

Stores user-defined expense categories.

**Schema:**
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439013"),
  "user_id": ObjectId("507f1f77bcf86cd799439011"),
  "name": "Groceries",
  "created_at": ISODate("2024-01-10T14:20:30.000Z")
}
```

**Field Descriptions:**
| Field | Type | Description |
|-------|------|-------------|
| `_id` | ObjectId | Unique category ID |
| `user_id` | ObjectId | References `users._id` (ownership) |
| `name` | String | Category name (e.g., "Groceries") |
| `created_at` | DateTime | When category was created |

**Indexes:**
```javascript
db.categories.createIndex({ "user_id": 1 })
```

**Default Categories (Hard-coded):**
```
Food
Fuel
Gas
Education
Travel
Office Supplies
Utilities
Other
```

**Sample Insert:**
```javascript
db.categories.insertOne({
  "user_id": ObjectId("507f1f77bcf86cd799439011"),
  "name": "Groceries",
  "created_at": new Date()
})
```

---

## Data Relationships & Isolation

```
users (1)
  ├── expenses (N) ─── referenced by user_id
  └── categories (N) ─ referenced by user_id
```

**User Isolation Example:**

User A (ID: `111...`) → sees only expenses where `user_id == 111...`  
User B (ID: `222...`) → sees only expenses where `user_id == 222...`

```javascript
// User A's query
db.expenses.find({ "user_id": ObjectId("111...") })
// Result: 5 expenses

// User B's query  
db.expenses.find({ "user_id": ObjectId("222...") })
// Result: 3 expenses (different data!)
```

---

## Sample Data

### Create Test Data:

```javascript
// Create user
const userId = db.users.insertOne({
  "email": "john@example.com",
  "full_name": "John Doe",
  "password_hash": "$2b$12$...",
  "created_at": new Date(),
  "updated_at": new Date()
}).insertedId

// Add some expenses for John
db.expenses.insertMany([
  {
    "user_id": userId,
    "bill_name": "Grocery Store Receipt",
    "vendor": "Whole Foods",
    "category": "Food",
    "expense_type": "Personal",
    "amount": 125.50,
    "gst": 12.55,
    "date": "2024-01-15"
  },
  {
    "user_id": userId,
    "bill_name": "Uber Receipt",
    "vendor": "Uber",
    "category": "Travel",
    "expense_type": "Business",
    "amount": 45.00,
    "gst": 4.50,
    "date": "2024-01-14"
  }
])

// Add a custom category
db.categories.insertOne({
  "user_id": userId,
  "name": "Groceries",
  "created_at": new Date()
})
```

---

## Important Operations

### 1. **Verify User Isolation**

```javascript
// All of User A's data
db.expenses.find({ "user_id": ObjectId("507f1f77bcf86cd799439011") })

// Count User A's categories
db.categories.countDocuments({ "user_id": ObjectId("507f1f77bcf86cd799439011") })
```

### 2. **Find by Date Range**

```javascript
// Expenses in January 2024
db.expenses.find({
  "user_id": ObjectId("507f1f77bcf86cd799439011"),
  "date": { "$gte": "2024-01-01", "$lte": "2024-01-31" }
})
```

### 3. **Aggregate User Statistics**

```javascript
// Total expenses and GST by category for a user
db.expenses.aggregate([
  { "$match": { "user_id": ObjectId("507f1f77bcf86cd799439011") } },
  {
    "$group": {
      "_id": "$category",
      "total_amount": { "$sum": "$amount" },
      "total_gst": { "$sum": "$gst" },
      "count": { "$sum": 1 }
    }
  },
  { "$sort": { "total_amount": -1 } }
])
```

### 4. **Delete User & All Their Data**

```javascript
// Get user ID
const userId = ObjectId("507f1f77bcf86cd799439011")

// Delete user
db.users.deleteOne({ "_id": userId })

// Delete user's expenses
db.expenses.deleteMany({ "user_id": userId })

// Delete user's categories
db.categories.deleteMany({ "user_id": userId })
```

---

## Backup & Migration

### MongoDB Atlas Backup
- Automatic daily backups
- Available in Atlas console
- Can restore to any point in time

### Manual Export/Import
```bash
# Export collection as JSON
mongoexport --uri "mongodb+srv://..." --collection expenses --out expenses.json

# Import collection from JSON
mongoimport --uri "mongodb+srv://..." --collection expenses --file expenses.json
```

---

## Performance Considerations

1. **Indexes Speed Up Queries**
   - `user_id` index: Essential for filtering user data
   - `date` index: Important for date range queries
   - Composite `(user_id, date)`: Optimizes common queries

2. **Document Size Limits**
   - MongoDB max doc size: 16MB (plenty for expenses)
   - Typical expense doc: ~500 bytes

3. **Scalability**
   - MongoDB Atlas auto-scales
   - Suitable for 1M+ documents
   - Can handle 100+ concurrent users easily

---

## Security

1. **Connection String Security**
   - Stored in `backend/.env` (never committed to git)
   - Use strong MongoDB passwords
   - Whitelist IP addresses in MongoDB Atlas

2. **Data Encryption**
   - MongoDB Atlas: TLS/SSL encryption in transit
   - Optional: Encryption at rest

3. **User Isolation**
   - All queries include `user_id` filter in backend
   - Cannot query another user's data through API
   - Database enforces user boundaries

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Duplicate key error on email" | Email must be unique; check existing users |
| "Connection timeout" | Check MongoDB URL, firewall, IP whitelist |
| "Collection not found" | Collections auto-create on first insert |
| "Slow queries" | Add indexes: `db.collection.createIndex(...)` |

---

**For Additional Help:**
- MongoDB Docs: https://docs.mongodb.com/
- MongoDB Atlas: https://www.mongodb.com/cloud/atlas
- PyMongo: https://pymongo.readthedocs.io/

---

**Version:** 1.0.0  
**Last Updated:** May 6, 2026
