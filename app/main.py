"""
==========================================================
SkillForge Platform
Main Application
==========================================================
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.init_db import init_db

# ===========================
# API Routers
# ===========================

from app.routers import (
    auth,
    student,
    course,
    enrollment,
    web
)


# ==========================================================
# Application Lifespan
# ==========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize database on application startup.
    """
    init_db()
    yield


# ==========================================================
# FastAPI Application
# ==========================================================

app = FastAPI(
    title="SkillForge LMS API",
    description="Learning Management System built with FastAPI",
    version="1.0.0",
    lifespan=lifespan
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
# API Routers
# ==========================================================

app.include_router(auth.router)
app.include_router(student.router)
app.include_router(course.router)
app.include_router(enrollment.router)


# ==========================================================
# Web Routes (HTML Pages)
# ==========================================================

app.include_router(web.router)


# ==========================================================
# Health Check
# ==========================================================

@app.get("/health", tags=["Health"])
def health():
    """
    Health Check Endpoint
    """
    return {
        "status": "success",
        "message": "SkillForge LMS API is running."
    }