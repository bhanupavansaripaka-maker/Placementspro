"""
==========================================================
SkillForge Platform
Application Entry Point
==========================================================
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.database import Base, engine

# ==========================================================
# Register SQLAlchemy Models
# ==========================================================

from app.models.user import User
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.module import Module
from app.models.lesson import Lesson

# ==========================================================
# Routers
# ==========================================================

from app.routers import (
    home,
    auth,
    auth_pages,
    student,
    student_pages,
    course,
    enrollment,
    dashboard,
    contact,
    ai,
    admin
)

# ==========================================================
# Create Database Tables
# ==========================================================

Base.metadata.create_all(bind=engine)

# ==========================================================
# FastAPI Application
# ==========================================================

app = FastAPI(
    title="SkillForge LMS",
    description="Learning Management System built with FastAPI",
    version="1.0.0"
)

# ==========================================================
# Templates
# ==========================================================

templates = Jinja2Templates(
    directory="app/templates"
)

# ==========================================================
# Static Files
# ==========================================================

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

# ==========================================================
# Public Website Routers
# ==========================================================

app.include_router(home.router)
app.include_router(contact.router)

# ==========================================================
# HTML Pages
# ==========================================================

app.include_router(auth_pages.router)
app.include_router(student_pages.router)

# ==========================================================
# Student APIs
# ==========================================================

app.include_router(auth.router)
app.include_router(student.router)
app.include_router(course.router)
app.include_router(enrollment.router)
app.include_router(dashboard.router)

# ==========================================================
# AI APIs
# ==========================================================

app.include_router(ai.router)

# ==========================================================
# Admin Portal
# ==========================================================

app.include_router(admin.router)

# ==========================================================
# Health Check
# ==========================================================

@app.get("/health")
def health():

    return {
        "status": "OK",
        "application": "SkillForge LMS",
        "version": "1.0.0"
    }