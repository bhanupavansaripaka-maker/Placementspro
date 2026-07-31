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

from app.routers import (
    home,
    auth,
    auth_pages,
    student,
    student_pages,
    course,
    enrollment,
    dashboard,
    contact
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
# Routers
# ==========================================================

# -------------------------
# Public Website
# -------------------------

app.include_router(home.router)
app.include_router(contact.router)

# -------------------------
# HTML Pages
# -------------------------

app.include_router(auth_pages.router)
app.include_router(student_pages.router)

# -------------------------
# JSON APIs
# -------------------------

app.include_router(auth.router)
app.include_router(student.router)
app.include_router(course.router)
app.include_router(enrollment.router)
app.include_router(dashboard.router)

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