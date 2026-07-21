"""
==========================================================
SkillForge Platform
Courses Page Router
==========================================================
"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db

from app.services.home_service import get_home_page_data
from app.services.course_service import get_active_courses

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/courses", response_class=HTMLResponse)
def courses_page(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Render Courses Page
    """

    data = get_home_page_data()

    courses = get_active_courses(db)

    data["featured_courses"] = courses

    return templates.TemplateResponse(
        "pages/courses.html",
        {
            "request": request,
            "title": "Courses",
            "active_page": "courses",
            **data
        }
    )