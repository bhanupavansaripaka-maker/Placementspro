"""
==========================================================
SkillForge Platform
Dashboard Router
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

from app.schemas.dashboard import DashboardStatistics
from app.services.dashboard_service import DashboardService


templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    tags=["Dashboard"]
)

# ==========================================================
# Dashboard Page
# ==========================================================

@router.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard_page(request: Request):
    """
    Render Student Dashboard.
    """

    return templates.TemplateResponse(
        "dashboard/dashboard.html",
        {
            "request": request,
            "active_page": "dashboard"
        }
    )


# ==========================================================
# AI Course Builder Page
# ==========================================================

@router.get(
    "/dashboard/ai-course-builder",
    response_class=HTMLResponse
)
def ai_course_builder_page(request: Request):
    """
    Render AI Course Builder page.
    """

    return templates.TemplateResponse(
        "dashboard/ai_course_builder.html",
        {
            "request": request,
            "active_page": "ai-course-builder"
        }
    )


# ==========================================================
# Dashboard Statistics API
# ==========================================================

@router.get(
    "/api/dashboard/statistics",
    response_model=DashboardStatistics
)
def get_dashboard_statistics(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Return dashboard statistics.
    """

    try:

        return DashboardService.get_statistics(
            db=db,
            student_id=student_id
        )

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch dashboard statistics."
        )


# ==========================================================
# Continue Learning API
# ==========================================================

@router.get("/api/dashboard/continue-learning")
def get_continue_learning(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Return the student's most recently enrolled course.
    """

    try:

        course = DashboardService.get_continue_learning(
            db=db,
            student_id=student_id
        )

        if course is None:
            return None

        return {
            "course_id": course.id,
            "title": course.title,
            "category": course.category,
            "level": course.level,
            "duration": course.duration,
            "price": course.price
        }

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch continue learning course."
        )