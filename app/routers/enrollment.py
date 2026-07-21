"""
==========================================================
SkillForge Platform
Enrollment API Router
==========================================================
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.enrollment import (
    EnrollmentCreate,
    EnrollmentResponse,
    StudentCourseResponse
)

from app.services.enrollment_service import (
    enroll_student,
    get_student_courses
)

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
    status_code=201
)
def create_enrollment(
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db)
):

    return enroll_student(
        db,
        enrollment.student_id,
        enrollment.course_id
    )


# ==========================================================
# Student Courses
# ==========================================================

@router.get(
    "/student/{student_id}",
    response_model=list[StudentCourseResponse]
)
def student_courses(
    student_id: int,
    db: Session = Depends(get_db)
):

    return get_student_courses(
        db,
        student_id
    )