"""
==========================================================
SkillForge Platform
Student Service
==========================================================
"""

from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.user import User
from app.schemas.student import StudentProfileCreate


def create_student_profile(
    db: Session,
    current_user: User,
    profile: StudentProfileCreate
):
    """
    Create a student profile.
    """

    existing = (
        db.query(Student)
        .filter(Student.user_id == current_user.id)
        .first()
    )

    if existing:
        raise ValueError("Student profile already exists.")

    student = Student(
        user_id=current_user.id,
        phone=profile.phone,
        college=profile.college,
        branch=profile.branch,
        graduation_year=profile.graduation_year,
        profile_photo=profile.profile_photo,
        resume=profile.resume
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return student


def get_student_profile(
    db: Session,
    current_user: User
):
    """
    Get the logged-in student's profile.
    """

    return (
        db.query(Student)
        .filter(Student.user_id == current_user.id)
        .first()
    )