from datetime import datetime, timedelta
from typing import Dict, Optional
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET", "your-super-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200  # 30 days

def create_access_token(data: Dict) -> str:
    """
    Create a JWT access token
    """
    to_encode = data.copy()
    if "exp" not in to_encode:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> Dict:
    """
    Verify and decode a JWT access token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise Exception(f"Token verification failed: {str(e)}")

def decode_token(token: str) -> Optional[Dict]:
    """
    Decode a token without verification (for debugging)
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None