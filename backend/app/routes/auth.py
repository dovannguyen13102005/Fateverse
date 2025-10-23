from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from google.oauth2 import id_token
from google.auth.transport import requests
from datetime import datetime, timedelta
from typing import Dict
from ..models.user import UserCreate, UserResponse
from ..database.mongodb import users
from ..utils.jwt import create_access_token, verify_access_token
from ..utils.password import hash_password, verify_password
from pydantic import BaseModel, EmailStr
import os
from bson import ObjectId

router = APIRouter()

# OAuth2 scheme for dependency injection
oauth2_scheme = HTTPBearer()

class GoogleLoginRequest(BaseModel):
    credential: str

class EmailLoginRequest(BaseModel):
    email: EmailStr
    password: str

class EmailRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    birth_date: str = None
    gender: str = None

class LoginResponse(BaseModel):
    user: UserResponse
    token: str
    message: str

# Dependency to get current user ID from JWT token
async def get_current_user_id(credentials = Depends(oauth2_scheme)):
    try:
        token = credentials.credentials
        payload = verify_access_token(token)
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return user_id
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid authentication credentials: {str(e)}")

@router.post("/google", response_model=LoginResponse)
async def google_login(request: GoogleLoginRequest):
    try:
        # Verify the Google ID token
        google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        if not google_client_id:
            raise HTTPException(status_code=500, detail="Google Client ID not configured")
        
        # Verify the token
        idinfo = id_token.verify_oauth2_token(
            request.credential, 
            requests.Request(), 
            google_client_id
        )
        
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        
        # Extract user information
        google_id = idinfo['sub']
        email = idinfo['email']
        name = idinfo['name']
        picture = idinfo.get('picture', '')
        
        # Check if user exists
        existing_user = await users.find_one({"email": email})
        
        if existing_user:
            # Update user info if needed
            update_data = {
                "name": name,
                "picture": picture,
                "last_login": datetime.now()
            }
            await users.update_one(
                {"email": email},
                {"$set": update_data}
            )
            user_data = {**existing_user, **update_data}
        else:
            # Create new user
            user_data = {
                "id": str(ObjectId()),
                "google_id": google_id,
                "email": email,
                "name": name,
                "picture": picture,
                "theme_preference": "galaxy",
                "created_at": datetime.now(),
                "last_login": datetime.now()
            }
            await users.insert_one(user_data)
        
        # Create JWT token
        token_data = {
            "user_id": user_data["id"],
            "email": user_data["email"],
            "exp": datetime.utcnow() + timedelta(days=30)
        }
        access_token = create_access_token(token_data)
        
        # Prepare user response
        user_response = UserResponse(
            id=user_data["id"],
            name=user_data["name"],
            email=user_data["email"],
            picture=user_data.get("picture", ""),
            theme_preference=user_data.get("theme_preference", "galaxy"),
            created_at=user_data["created_at"]
        )
        
        return LoginResponse(
            user=user_response,
            token=access_token,
            message="Đăng nhập thành công"
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid Google token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")

@router.post("/logout")
async def logout():
    # In a real implementation, you might want to blacklist the token
    return {"message": "Đăng xuất thành công"}

@router.post("/register", response_model=LoginResponse)
async def register_with_email(request: EmailRegisterRequest):
    """Register a new user with email and password"""
    try:
        # Check if email already exists
        existing_user = await users.find_one({"email": request.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email đã được đăng ký")
        
        # Hash the password
        hashed_password = hash_password(request.password)
        
        # Create new user
        user_data = {
            "id": str(ObjectId()),
            "email": request.email,
            "hashed_password": hashed_password,
            "name": request.name,
            "birth_date": request.birth_date,
            "gender": request.gender,
            "picture": "",
            "theme_preference": "galaxy",
            "created_at": datetime.now(),
            "last_login": datetime.now()
        }
        
        await users.insert_one(user_data)
        
        # Create JWT token
        token_data = {
            "user_id": user_data["id"],
            "email": user_data["email"],
            "exp": datetime.utcnow() + timedelta(days=30)
        }
        access_token = create_access_token(token_data)
        
        # Prepare user response (don't include password)
        user_response = UserResponse(
            id=user_data["id"],
            name=user_data["name"],
            email=user_data["email"],
            picture=user_data.get("picture", ""),
            theme_preference=user_data.get("theme_preference", "galaxy"),
            created_at=user_data["created_at"]
        )
        
        return LoginResponse(
            user=user_response,
            token=access_token,
            message="Đăng ký thành công"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Đăng ký thất bại: {str(e)}")

@router.post("/login", response_model=LoginResponse)
async def login_with_email(request: EmailLoginRequest):
    """Login with email and password"""
    try:
        # Find user by email
        user = await users.find_one({"email": request.email})
        if not user:
            raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng")
        
        # Check if user has password (not Google-only account)
        if "hashed_password" not in user or not user["hashed_password"]:
            raise HTTPException(
                status_code=400, 
                detail="Tài khoản này đã đăng ký bằng Google. Vui lòng đăng nhập bằng Google."
            )
        
        # Verify password
        if not verify_password(request.password, user["hashed_password"]):
            raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng")
        
        # Update last login
        await users.update_one(
            {"email": request.email},
            {"$set": {"last_login": datetime.now()}}
        )
        user["last_login"] = datetime.now()
        
        # Create JWT token
        token_data = {
            "user_id": user["id"],
            "email": user["email"],
            "exp": datetime.utcnow() + timedelta(days=30)
        }
        access_token = create_access_token(token_data)
        
        # Prepare user response
        user_response = UserResponse(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            picture=user.get("picture", ""),
            theme_preference=user.get("theme_preference", "galaxy"),
            created_at=user["created_at"]
        )
        
        return LoginResponse(
            user=user_response,
            token=access_token,
            message="Đăng nhập thành công"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Đăng nhập thất bại: {str(e)}")

@router.get("/verify")
async def verify_token(user_id: str = Depends(get_current_user_id)):
    """Verify if the current token is valid"""
    user = await users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=user["id"],
        name=user["name"],
        email=user["email"],
        picture=user.get("picture", ""),
        theme_preference=user.get("theme_preference", "galaxy"),
        created_at=user["created_at"]
    )