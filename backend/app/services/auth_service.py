"""Authentication service for user management and JWT handling."""
import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional
from bson.objectid import ObjectId
from app.utils.db import get_users_collection
from app.models.schemas import UserResponse, TokenPayload

# JWT Configuration
JWT_SECRET = "your-secret-key-change-in-production"  # Will be overridden by environment variable
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24


def set_jwt_secret(secret: str) -> None:
    """Set JWT secret from environment."""
    global JWT_SECRET
    JWT_SECRET = secret


def hash_password(password: str) -> str:
    """Hash password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash.
    
    Args:
        password: Plain text password to verify
        password_hash: Stored password hash
        
    Returns:
        True if password matches, False otherwise
    """
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token.
    
    Args:
        user_id: User ObjectId as string
        expires_delta: Custom expiration time (default 24 hours)
        
    Returns:
        JWT token
    """
    if expires_delta is None:
        expires_delta = timedelta(hours=JWT_EXPIRATION_HOURS)
    
    expire = datetime.utcnow() + expires_delta
    payload = {
        "user_id": user_id,
        "exp": expire,
        "iat": datetime.utcnow()
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_token(token: str) -> Optional[TokenPayload]:
    """Decode and validate JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        TokenPayload with user_id, or None if invalid
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            return None
        return TokenPayload(user_id=user_id, exp=payload.get("exp"))
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_user_by_email(email: str) -> Optional[dict]:
    """Get user from database by email.
    
    Args:
        email: User email
        
    Returns:
        User document or None
    """
    users = get_users_collection()
    user = users.find_one({"email": email})
    return user


def get_user_by_id(user_id: str) -> Optional[dict]:
    """Get user from database by ID.
    
    Args:
        user_id: User ObjectId as string
        
    Returns:
        User document or None
    """
    try:
        users = get_users_collection()
        user = users.find_one({"_id": ObjectId(user_id)})
        return user
    except Exception:
        return None


def create_user(email: str, password: str, full_name: str) -> Optional[str]:
    """Create new user in database.
    
    Args:
        email: User email (must be unique)
        password: Plain text password (will be hashed)
        full_name: User's full name
        
    Returns:
        User ID (ObjectId as string) or None if creation failed
    """
    # Check if user already exists
    if get_user_by_email(email):
        return None
    
    users = get_users_collection()
    password_hash = hash_password(password)
    now = datetime.utcnow()
    
    user_doc = {
        "email": email,
        "password_hash": password_hash,
        "full_name": full_name,
        "created_at": now,
        "updated_at": now
    }
    
    result = users.insert_one(user_doc)
    return str(result.inserted_id)


def authenticate_user(email: str, password: str) -> Optional[dict]:
    """Authenticate user by email and password.
    
    Args:
        email: User email
        password: Plain text password
        
    Returns:
        User document if credentials valid, None otherwise
    """
    user = get_user_by_email(email)
    if not user:
        return None
    
    if not verify_password(password, user.get("password_hash", "")):
        return None
    
    return user


def user_to_response(user: dict) -> UserResponse:
    """Convert user document to UserResponse (excludes password).
    
    Args:
        user: User document from MongoDB
        
    Returns:
        UserResponse object
    """
    return UserResponse(
        id=str(user["_id"]),
        email=user["email"],
        full_name=user["full_name"]
    )
