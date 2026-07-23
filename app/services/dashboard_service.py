"""
==========================================================
SkillForge Platform
Dashboard Service
==========================================================
"""

from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.student import Student


class DashboardService:
    """
    Service class for dashboard operations.
    """

    @staticmethod
    def get_statistics(
        db: Session,
        student_id: int
    ) -> dict:
        """
        Returns dashboard statistics.
        """

        # ----------------------------------------
        # Enrolled Courses
        # ----------------------------------------

        enrolled_courses = (
            db.query(Enrollment)
            .filter(
                Enrollment.student_id == student_id
            )
            .count()
        )

        # ----------------------------------------
        # Available Courses
        # ----------------------------------------

        available_courses = (
            db.query(Course)
            .filter(
                Course.is_active == True
            )
            .count()
        )

        # ----------------------------------------
        # Categories
        # ----------------------------------------

        categories = (
            db.query(Course.category)
            .distinct()
            .count()
        )

        # ----------------------------------------
        # Profile Status
        # ----------------------------------------

        student = (
            db.query(Student)
            .filter(
                Student.id == student_id
            )
            .first()
        )

        profile_completed = student is not None

        return {
            "enrolled_courses": enrolled_courses,
            "available_courses": available_courses,
            "categories": categories,
            "profile_completed": profile_completed
        }