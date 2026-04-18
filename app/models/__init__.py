from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    # Using lambda to ensure time is captured at insertion, not app startup
    created_at = Column(String(50), default=lambda: datetime.now(timezone.utc).isoformat())
    
    applications = relationship("Application", back_populates="user")
    jobs = relationship("Job", back_populates="created_by")

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=False)
    location = Column(String(100), nullable=False)
    salary = Column(String(50), nullable=False)
    is_active = Column(Integer, default=1)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(String(50), default=lambda: datetime.now(timezone.utc).isoformat())
    
    created_by = relationship("User", back_populates="jobs")
    applications = relationship("Application", back_populates="job")

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    cover_letter = Column(Text, nullable=True)
    applied_at = Column(String(50), default=lambda: datetime.now(timezone.utc).isoformat())
    
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")