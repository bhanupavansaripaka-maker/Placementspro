"""
==========================================================
SkillForge Platform
Course API Router
==========================================================
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.course import (
    CourseCreate,
    CourseResponse
)

from app.services.course_service import CourseService


router = APIRouter(
    prefix="/api/courses",
    tags=["Course Management"]
)


# ==========================================================
# Create Course
# ==========================================================

@router.post(
    "/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED
)
def add_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new course.
    """

    try:

        return CourseService.create(
            db,
            course
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create course."
        )


# ==========================================================
# Get All Courses
# ==========================================================

@router.get(
    "/",
    response_model=list[CourseResponse]
)
def list_courses(
    db: Session = Depends(get_db)
):
    """
    Get all courses.
    """

    return CourseService.get_all(db)
# ==========================================================
# Get Course By ID
# ==========================================================

@router.get(
    "/{course_id}",
    response_model=CourseResponse
)
def get_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    """
    Return a single course.
    """

    course = CourseService.get_by_id(
        db,
        course_id
    )

    if course is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found."
        )

    return course