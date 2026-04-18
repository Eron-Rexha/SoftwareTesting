import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .database import engine, Base
from .routers import router as api_router

# 1. Setup the Base Directory and Template engine correctly
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# 2. Initialize the App
app = FastAPI(
    title="CareerStream Pro - Opportunity Management System",
    description="""
    ## Professional Career Management API
    This API handles the full lifecycle of job postings and applications.
    """,
    version="1.0.0",
)

# 3. Initialize database tables
Base.metadata.create_all(bind=engine)

# 4. Include Routers
app.include_router(api_router)

# 5. Frontend Routes (Home, Signup, and Signin)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/signin", response_class=HTMLResponse)
async def signin_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})