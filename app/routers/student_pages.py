"""
==========================================================
SkillForge LMS
Student Pages Router
==========================================================
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    tags=["Student Pages"]
)

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get(
    "/my-courses",
    response_class=HTMLResponse
)
async def my_courses_page(
    request: Request
):
    """
    Render My Courses page.
    """

    return templates.TemplateResponse(
        "student/my_courses.html",
        {
            "request": request
        }
    )


@router.get(
    "/profile",
    response_class=HTMLResponse
)
async def profile_page(
    request: Request
):
    """
    Render Student Profile page.
    """

    return templates.TemplateResponse(
        "student/profile.html",
        {
            "request": request
        }
    )
# ==========================================================
# Student Profile Page
# ==========================================================

@router.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    """
    Render Student Profile Page.
    """

    return templates.TemplateResponse(
        "student/profile.html",
        {
            "request": request,
            "active_page": "profile"
        }
    )
# ==========================================================
# Course Details Page
# ==========================================================

@router.get(
    "/course/{course_id}",
    response_class=HTMLResponse
)
async def course_details_page(
    request: Request,
    course_id: int
):
    """
    Render Course Details page.
    """

    return templates.TemplateResponse(
        "course/course_details.html",
        {
            "request": request,
            "course_id": course_id,
            "active_page": "courses"
        }
    )