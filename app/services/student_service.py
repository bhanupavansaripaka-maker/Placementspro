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


def update_student_profile(
    db: Session,
    current_user: User,
    profile: StudentProfileCreate
):
    """
    Create or update the logged-in student's profile.
    """

    student = (
        db.query(Student)
        .filter(Student.user_id == current_user.id)
        .first()
    )

    # Safety check (normally the Student is created during registration)
    if not student:
        student = Student(
            user_id=current_user.id
        )
        db.add(student)

    # Update profile fields
    student.phone = profile.phone
    student.college = profile.college
    student.education = profile.education
    student.branch = profile.branch
    student.graduation_year = profile.graduation_year
    student.profile_photo = profile.profile_photo
    student.resume = profile.resume

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