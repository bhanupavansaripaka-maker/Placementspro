"""
==========================================================
SkillForge Platform
Enrollment API Router
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

from app.schemas.enrollment import (
    EnrollmentCreate,
    EnrollmentResponse,
    StudentCourseResponse
)

from app.services.enrollment_service import EnrollmentService


router = APIRouter(
    prefix="/api/enrollments",
    tags=["Enrollment Management"]
)


# ==========================================================
# Enroll Student
# ==========================================================

@router.post(
    "/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_enrollment(
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db)
):
    """
    Enroll a student into a course.
    """

    try:

        enrolled = EnrollmentService.enroll(
            db,
            enrollment.student_id,
            enrollment.course_id
        )

        if enrolled is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student or Course not found."
            )

        return enrolled

    except HTTPException:
        raise

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create enrollment."
        )


# ==========================================================
# Get Student Courses
# ==========================================================

@router.get(
    "/student/{student_id}",
    response_model=list[StudentCourseResponse]
)
def get_student_courses(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all courses enrolled by a student.
    """

    try:

        return EnrollmentService.get_student_courses(
            db,
            student_id
        )

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch enrolled courses."
        )