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


class StudentService:
    """
    Student Service
    """

    @staticmethod
    def update_profile(
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

        # Safety check
        if not student:

            student = Student(
                user_id=current_user.id
            )

            db.add(student)

        # ----------------------------------------
        # Update Profile
        # ----------------------------------------

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

    @staticmethod
    def get_profile(
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