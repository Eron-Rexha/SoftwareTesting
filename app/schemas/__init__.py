from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

# --- USER SCHEMAS ---
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)

# --- TOKEN SCHEMAS ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- JOB SCHEMAS ---
class JobCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    requirements: str = Field(min_length=1)
    location: str = Field(min_length=1, max_length=100)
    salary: str = Field(min_length=1, max_length=50)

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    is_active: Optional[bool] = None

class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    requirements: str
    location: str
    salary: str
    is_active: bool
    created_by_id: int

    model_config = ConfigDict(from_attributes=True)

# --- APPLICATION SCHEMAS ---
class ApplicationCreate(BaseModel):
    cover_letter: str = Field(min_length=1)

class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    applicant_id: int
    cover_letter: str
    status: str

    model_config = ConfigDict(from_attributes=True)
