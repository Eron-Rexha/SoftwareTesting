from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from ..database import get_db
from ..models import User, Job, Application
from ..schemas import (
    UserCreate, UserResponse, JobCreate, JobResponse, 
    ApplicationCreate, ApplicationResponse
)
from ..services import (
    hash_password, verify_password, create_access_token, get_current_user
)

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check for existing user
    stmt = select(User).where((User.username == user_data.username) | (User.email == user_data.email))
    if db.execute(stmt).first():
        raise HTTPException(status_code=400, detail="Username or email already exists")

    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.username == form_data.username)).scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    return {"access_token": create_access_token({"sub": user.username}), "token_type": "bearer"}

@router.get("/jobs", response_model=List[JobResponse])
async def get_jobs(db: Session = Depends(get_db)):
    return db.execute(select(Job).where(Job.is_active == 1)).scalars().all()

@router.post("/jobs", response_model=JobResponse, status_code=201)
async def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_job = Job(**job_data.model_dump(), created_by_id=current_user.id)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.delete("/jobs/{job_id}", status_code=204)
async def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job.is_active = 0
    db.commit()

@router.post("/jobs/{job_id}/apply", response_model=ApplicationResponse, status_code=201)
async def apply_to_job(
    job_id: int,
    app_data: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 1. Verify the job exists
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    new_app = Application(
        user_id=current_user.id, 
        job_id=job_id, 
        cover_letter=app_data.cover_letter
    )
    
    db.add(new_app)
    db.commit()
    db.refresh(new_app)

    # 3. Explicitly return response
    return ApplicationResponse(
        id=new_app.id,
        job_id=new_app.job_id,
        applicant_id=new_app.user_id, 
        cover_letter=new_app.cover_letter,
        status="pending"
    )
