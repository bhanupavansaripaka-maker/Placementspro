from fastapi import APIRouter
from fastapi import Form
from fastapi import Request

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/contact",
    tags=["Contact"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def contact_page(request: Request):

    return templates.TemplateResponse(
        "contact.html",
        {
                "request": request,
                "title": "Contact",
                "active_page": "contact"

        }
    )


@router.post("/")
async def submit_contact(

    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    message: str = Form(...)

):

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