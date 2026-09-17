"""
==========================================================
PlacementsPro
Application Entry Point
==========================================================
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.database import Base, engine


# ==========================================================
# Import Models
# ==========================================================

from app.models.course import Course
from app.models.module import Module
from app.models.lesson import Lesson
from app.models.lesson_content import LessonContent
from app.models.quiz import Quiz, QuizQuestion
from app.models.quiz_attempt import QuizAttempt


# ==========================================================
# Import Routers
# ==========================================================

from app.routers.admin import router as admin_router
from app.routers.ai import router as ai_router

from app.routers.auth import router as auth_router
from app.routers.auth_pages import router as auth_pages_router

from app.routers.contact import router as contact_router
from app.routers.course import router as course_router
from app.routers.courses import router as courses_router

from app.routers.dashboard import router as dashboard_router
from app.routers.enrollment import router as enrollment_router
from app.routers.home import router as home_router

from app.routers.student import router as student_router
from app.routers.student_pages import (
    router as student_pages_router
)

from app.routers.learning import router as learning_router
from app.routers.quiz import router as quiz_router


# ==========================================================
# Create Database Tables
# ==========================================================

Base.metadata.create_all(
    bind=engine
)


# ==========================================================
# Create FastAPI Application
# ==========================================================

app = FastAPI(
    title="PlacementsPro",
    description="AI Powered Learning Management System",
    version="1.0.0"
)


# ==========================================================
# Static Files
# ==========================================================

app.mount(
    "/static",
    StaticFiles(
        directory="app/static"
    ),
    name="static"
)


# ==========================================================
# Register Routers
# ==========================================================

app.include_router(home_router)

app.include_router(auth_router)
app.include_router(auth_pages_router)

app.include_router(contact_router)

app.include_router(course_router)
app.include_router(courses_router)

app.include_router(dashboard_router)

app.include_router(enrollment_router)

app.include_router(student_router)
app.include_router(student_pages_router)

app.include_router(learning_router)

app.include_router(quiz_router)

app.include_router(ai_router)

app.include_router(admin_router)


# ==========================================================
# Root Health Check
# ==========================================================

@app.get(
    "/health",
    tags=["System"]
)
def health_check():

    return {
        "status": "healthy",
        "application": "PlacementsPro",
        "version": "1.0.0"
    }