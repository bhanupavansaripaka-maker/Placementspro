"""
==========================================================
SkillForge Platform
Student Service
==========================================================
"""

from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.user import User

from app.schemas.student import (
    StudentProfileCreate,
    StudentProfileUpdate
)


class StudentService:
    """
    Student Service
    """

    # ==========================================================
    # Get Student Profile
    # ==========================================================

    @staticmethod
    def get_profile(
        db: Session,
        current_user: User
    ) -> Student | None:
        """
        Return logged-in student's profile.
        """

        return (
            db.query(Student)
            .filter(
                Student.user_id == current_user.id
            )
            .first()
        )

    # ==========================================================
    # Create Student Profile
    # ==========================================================

    @staticmethod
    def create_profile(
        db: Session,
        current_user: User,
        profile: StudentProfileCreate
    ) -> Student:
        """
        Create student profile if it doesn't exist.
        """

        student = (
            db.query(Student)
            .filter(
                Student.user_id == current_user.id
            )
            .first()
        )

        if student:

            return student

        student = Student(
            user_id=current_user.id,
            phone=profile.phone,
            college=profile.college,
            education=profile.education,
            branch=profile.branch,
            graduation_year=profile.graduation_year,
            profile_photo=profile.profile_photo,
            resume=profile.resume
        )

        db.add(student)
        db.commit()
        db.refresh(student)

        return student

    # ==========================================================
    # Update Student Profile
    # ==========================================================

    @staticmethod
    def update_profile(
        db: Session,
        current_user: User,
        profile: StudentProfileUpdate
    ) -> Student:
        """
        Update logged-in student's profile.
        """

        student = (
            db.query(Student)
            .filter(
                Student.user_id == current_user.id
            )
            .first()
        )

        if not student:

            student = Student(
                user_id=current_user.id
            )

            db.add(student)

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