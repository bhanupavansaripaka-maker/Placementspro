"""
==========================================================
Student Router
==========================================================
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User

from app.schemas.student import (
    StudentProfileCreate,
    StudentProfileResponse
)

from app.services.student_service import (
    create_student_profile,
    get_student_profile
)

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.post("/profile")
def create_profile(
    profile: StudentProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    try:

        student = create_student_profile(
            db,
            current_user,
            profile
        )

        return {
            "message": "Student profile created successfully.",
            "student_id": student.id
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get(
    "/profile",
    response_model=StudentProfileResponse
)
def read_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    student = get_student_profile(
        db,
        current_user
    )

    if student is None:

        raise HTTPException(
            status_code=404,
            detail="Student profile not found."
        )

    return {
        "id": student.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "phone": student.phone,
        "college": student.college,
        "branch": student.branch,
        "graduation_year": student.graduation_year,
        "profile_photo": student.profile_photo,
        "resume": student.resume
    }