"""
==========================================================
SkillForge LMS
Admin Router
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

from app.schemas.admin import (
    AdminDashboardStatistics,
    UpdateCourseRequest
)

from app.schemas.ai import CurriculumSaveRequest

from app.services.admin_service import AdminService
from app.services.ai.curriculum_service import CurriculumService

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

templates = Jinja2Templates(
    directory="app/templates"
)

# ==========================================================
# Admin Dashboard Page
# ==========================================================

@router.get(
    "/dashboard",
    response_class=HTMLResponse
)
def admin_dashboard(request: Request):

    return templates.TemplateResponse(
        "admin/dashboard.html",
        {
            "request": request,
            "active_page": "dashboard"
        }
    )


# ==========================================================
# AI Content Studio
# ==========================================================

@router.get(
    "/ai-course-builder",
    response_class=HTMLResponse
)
def ai_course_builder(request: Request):

    return templates.TemplateResponse(
        "admin/ai_course_builder.html",
        {
            "request": request,
            "active_page": "ai-course-builder"
        }
    )


# ==========================================================
# Dashboard Statistics API
# ==========================================================

@router.get(
    "/api/dashboard",
    response_model=AdminDashboardStatistics
)
def get_dashboard_statistics(
    db: Session = Depends(get_db)
):

    try:

        return AdminService.get_dashboard_statistics(db)

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ==========================================================
# Course Management Page
# ==========================================================

@router.get(
    "/courses",
    response_class=HTMLResponse
)
def courses_page(request: Request):

    return templates.TemplateResponse(
        "admin/courses.html",
        {
            "request": request,
            "active_page": "courses"
        }
    )


# ==========================================================
# Get All Courses
# ==========================================================

@router.get("/api/courses")
def get_courses(
    db: Session = Depends(get_db)
):

    courses = AdminService.get_courses(db)

    return [

        {
            "id": course.id,
            "title": course.title,
            "category": course.category,
            "level": course.level,
            "duration": course.duration,
            "price": course.price,
            "is_active": course.is_active
        }

        for course in courses

    ]


# ==========================================================
# Course Details Page
# ==========================================================

@router.get(
    "/course/{course_id}",
    response_class=HTMLResponse
)
def course_detail_page(
    request: Request,
    course_id: int
):

    return templates.TemplateResponse(
        "admin/course_detail.html",
        {
            "request": request,
            "course_id": course_id,
            "active_page": "courses"
        }
    )


# ==========================================================
# Get Course Details API
# ==========================================================

@router.get("/api/course/{course_id}")
def get_course(
    course_id: int,
    db: Session = Depends(get_db)
):

    course = AdminService.get_course(
        db=db,
        course_id=course_id
    )

    if not course:

        raise HTTPException(
            status_code=404,
            detail="Course not found."
        )

    return {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "category": course.category,
        "level": course.level,
        "duration": course.duration,
        "price": course.price,
        "is_active": course.is_active,
        "modules": [
            {
                "id": module.id,
                "title": module.title,
                "description": module.description,
                "display_order": module.display_order,
                "lessons": [
                    {
                        "id": lesson.id,
                        "title": lesson.title,
                        "topic": lesson.topic,
                        "difficulty": lesson.difficulty,
                        "estimated_minutes": lesson.estimated_minutes
                    }
                    for lesson in module.lessons
                ]
            }
            for module in course.modules
        ]
    }


# ==========================================================
# Update Course API
# ==========================================================

@router.put("/api/course/{course_id}")
def update_course(
    course_id: int,
    request: UpdateCourseRequest,
    db: Session = Depends(get_db)
):
    """
    Update course information.
    """

    try:

        course = AdminService.update_course(
            db=db,
            course_id=course_id,
            data=request.model_dump()
        )

        if not course:

            raise HTTPException(
                status_code=404,
                detail="Course not found."
            )

        return {
            "success": True,
            "message": "Course updated successfully."
        }

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ==========================================================
# Save AI Curriculum
# ==========================================================

@router.post("/api/save-curriculum")
def save_curriculum(
    request: CurriculumSaveRequest,
    db: Session = Depends(get_db)
):

    try:

        result = CurriculumService.save_curriculum(
            db=db,
            curriculum=request.curriculum,
            difficulty=request.difficulty,
            duration=request.duration
        )

        return result

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )