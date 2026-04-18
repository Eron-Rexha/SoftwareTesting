from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import declarative_base

# Configuration from Claude code
DATABASE_URL = "sqlite:///./job_board.db"
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)
SessionLocal = lambda: Session(bind=engine)
Base = declarative_base()

# Dependency logic
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()