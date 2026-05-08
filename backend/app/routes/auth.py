"""Authentication routes for signup, login, and user profile."""
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.schemas import SignupRequest, LoginRequest, TokenResponse, UserResponse
from app.services.auth_service import (
    create_user,
    authenticate_user,
    create_access_token,
    user_to_response,
)
from app.utils.auth_dependency import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest):
    """Register a new user.
    
    Args:
        request: SignupRequest with email, password, full_name
        
    Returns:
        TokenResponse with JWT token and user info
        
    Raises:
        HTTPException: 400 if email already exists or invalid data
    """
    # Validate input
    if not request.email or not request.password or not request.full_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email, password, and full name are required"
        )
    
    if len(request.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters"
        )
    
    # Create user
    user_id = create_user(request.email, request.password, request.full_name)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    # Create token
    access_token = create_access_token(user_id)
    
    # Get user from database to return complete info
    from app.services.auth_service import get_user_by_id
    user = get_user_by_id(user_id)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_to_response(user)
    )


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Authenticate user and return JWT token.
    
    Args:
        request: LoginRequest with email and password
        
    Returns:
        TokenResponse with JWT token and user info
        
    Raises:
        HTTPException: 401 if credentials invalid
    """
    # Authenticate user
    user = authenticate_user(request.email, request.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create token
    access_token = create_access_token(str(user["_id"]))
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_to_response(user)
    )


@router.get("/me", response_model=UserResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile.
    
    Args:
        current_user: Current authenticated user (injected via dependency)
        
    Returns:
        UserResponse with user info
    """
    return user_to_response(current_user)


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """Logout endpoint (token-based, just returns success).
    
    Frontend should delete token from localStorage on receiving this response.
    
    Args:
        current_user: Current authenticated user (validates token is valid)
        
    Returns:
        Success message
    """
    return {"message": "Logged out successfully"}
