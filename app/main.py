"""
==========================================================
SkillForge Platform
Main Application
==========================================================
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import (
    APP_NAME,
    APP_DESCRIPTION,
    VERSION
)

# Routers
from app.routers.home import router as home_router
from app.routers.courses import router as courses_router
from app.routers.contact import router as contact_router
from app.routers.auth import router as auth_router


app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=VERSION
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

app.include_router(home_router)
app.include_router(courses_router)
app.include_router(contact_router)
app.include_router(auth_router)


# ==========================================================
# Health Check
# ==========================================================

@app.get("/health", tags=["Health"])
def health():
    """
    Health check endpoint.
    """

    return {
        "application": APP_NAME,
        "version": VERSION,
        "status": "Running"
    }