"""
==========================================================
SkillForge Platform
Courses Router
==========================================================
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status
)

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.database import get_db

from app.services.home_service import get_home_page_data
from app.services.course_service import CourseService


# ==========================================================
# Router
# ==========================================================

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


# ==========================================================
# Courses Page
# ==========================================================

@router.get(
    "/courses",
    response_class=HTMLResponse
)
def courses_page(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Render public Courses Page.
    """

    data = get_home_page_data()

    courses = CourseService.get_active(db)

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


# ==========================================================
# Student Course Details Page
# ==========================================================

@router.get(
    "/course/{course_id}",
    response_class=HTMLResponse
)
def course_detail_page(
    request: Request,
    course_id: int,
    db: Session = Depends(get_db)
):
    """
    Render student-facing course details page.
    """

    course = CourseService.get_by_id(
        db=db,
        course_id=course_id
    )

    # ------------------------------------------------------
    # Course Not Found
    # ------------------------------------------------------

    if not course:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found."
        )

    # ------------------------------------------------------
    # Inactive Course
    # ------------------------------------------------------

    if not course.is_active:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course is not available."
        )

    # ------------------------------------------------------
    # Render Page
    # ------------------------------------------------------

    return templates.TemplateResponse(
        "pages/course_detail.html",
        {
            "request": request,
            "title": course.title,
            "active_page": "courses",
            "course_id": course.id
        }
    )