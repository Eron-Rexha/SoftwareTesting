from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt
import os

# 1. Setup Password Hashing (using bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. JWT Configuration (Normally these come from environment variables)
SECRET_KEY = "my_super_secret_key_for_university_project"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(password: str) -> str:
    """Encodes a plain text password into a secure hash."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compares a plain text password with a stored hash."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generates a JWT token for user sessions."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt