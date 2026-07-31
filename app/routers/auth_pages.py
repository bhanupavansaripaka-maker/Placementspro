"""
==========================================================
SkillForge Platform
Authentication Pages Router
==========================================================
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    tags=["Authentication Pages"]
)


# ==========================================================
# Login Page
# ==========================================================

@router.get(
    "/login",
    response_class=HTMLResponse
)
def login_page(request: Request):
    """
    Render Login page.
    """

    return templates.TemplateResponse(
        "pages/login.html",
        {
            "request": request,
            "active_page": "login"
        }
    )


# ==========================================================
# Register Page
# ==========================================================

@router.get(
    "/register",
    response_class=HTMLResponse
)
def register_page(request: Request):
    """
    Render Registration page.
    """

    return templates.TemplateResponse(
        "pages/register.html",
        {
            "request": request,
            "active_page": "register"
        }
    )