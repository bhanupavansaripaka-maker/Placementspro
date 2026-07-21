"""
==========================================================
SkillForge Platform
Contact Page Router
==========================================================
"""

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.home_service import get_home_page_data

router = APIRouter(
    prefix="/contact",
    tags=["Contact"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def contact_page(request: Request):
    """
    Render Contact Page
    """

    data = get_home_page_data()

    return templates.TemplateResponse(
        "pages/contact.html",
        {
            "request": request,
            "title": "Contact",
            "active_page": "contact",
            **data
        }
    )


@router.post("/")
async def submit_contact(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    message: str = Form(...)
):
    """
    Process Contact Form
    """

    print("\n")
    print("=" * 60)
    print("NEW ENQUIRY")
    print("=" * 60)
    print(f"Name    : {name}")
    print(f"Email   : {email}")
    print(f"Phone   : {phone}")
    print(f"Message : {message}")
    print("=" * 60)

    return {
        "success": True,
        "message": "Thank you for contacting SkillForge LMS."
    }