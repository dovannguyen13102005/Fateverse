from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    birth_date: Optional[datetime] = None
    gender: Optional[str] = None
    theme_preference: Optional[str] = "galaxy"
    picture: Optional[str] = None

class UserCreate(UserBase):
    password: Optional[str] = None  # Optional for Google OAuth users
    google_id: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    birth_date: Optional[datetime] = None
    gender: Optional[str] = None
    theme_preference: Optional[str] = None
    picture: Optional[str] = None
    notification_enabled: Optional[bool] = None
    privacy_settings: Optional[dict] = None

class UserInDB(UserBase):
    id: str
    google_id: Optional[str] = None
    hashed_password: Optional[str] = None  # For email/password authentication
    created_at: datetime = datetime.now()
    last_login: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    picture: Optional[str] = None
    theme_preference: Optional[str] = "galaxy"
    created_at: datetime

    class Config:
        orm_mode = True