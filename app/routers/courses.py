from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.data.courses import courses

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def courses_page(request: Request):
    """
    Display the Courses page.
    """

    return templates.TemplateResponse(
        "pages/courses.html",
        {
            "request": request,
            "title": "Courses",
            "courses": courses,
            "active_page": "courses"
        }
    )


@router.get("/api")
async def get_courses():
    """
    Return all available courses as JSON.
    """

    return {
        "success": True,
        "count": len(courses),
        "data": courses
    }