"""
==========================================================
SkillForge Platform
Student Router
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
from app.core.security import get_current_user
from app.models.user import User

from app.schemas.student import (
    StudentProfileCreate,
    StudentProfileResponse
)

from app.services.student_service import (
    update_student_profile,
    get_student_profile
)

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.put(
    "/profile",
    response_model=StudentProfileResponse
)
def update_profile(
    profile: StudentProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create or update the logged-in student's profile.
    """

    try:

        student = update_student_profile(
            db,
            current_user,
            profile
        )

        return StudentProfileResponse(
            id=student.id,
            full_name=current_user.full_name,
            email=current_user.email,
            phone=student.phone,
            college=student.college,
            education=student.education,
            branch=student.branch,
            graduation_year=student.graduation_year,
            profile_photo=student.profile_photo,
            resume=student.resume
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong."
        )


@router.get(
    "/profile",
    response_model=StudentProfileResponse
)
def read_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get logged-in student's profile.
    """

    student = get_student_profile(
        db,
        current_user
    )

    if student is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found."
        )

    return StudentProfileResponse(
        id=student.id,
        full_name=current_user.full_name,
        email=current_user.email,
        phone=student.phone,
        college=student.college,
        education=student.education,
        branch=student.branch,
        graduation_year=student.graduation_year,
        profile_photo=student.profile_photo,
        resume=student.resume
    )