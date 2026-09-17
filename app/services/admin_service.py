"""
==========================================================
SkillForge LMS
Admin Service
==========================================================
"""

from sqlalchemy import func
from sqlalchemy.orm import (
    Session,
    joinedload
)

from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.module import Module


class AdminService:
    """
    Admin Dashboard Service
    """

    # ======================================================
    # Dashboard Statistics
    # ======================================================

    @staticmethod
    def get_dashboard_statistics(
        db: Session
    ):
        """
        Return dashboard statistics.
        """

        total_students = (
            db.query(func.count(Student.id))
            .scalar() or 0
        )

        total_courses = (
            db.query(func.count(Course.id))
            .scalar() or 0
        )

        total_enrollments = (
            db.query(func.count(Enrollment.id))
            .scalar() or 0
        )

        ai_generated_courses = (
            db.query(func.count(Module.id))
            .scalar() or 0
        )

        return {
            "students": total_students,
            "courses": total_courses,
            "enrollments": total_enrollments,
            "ai_generated": ai_generated_courses
        }


    # ======================================================
    # Get All Courses
    # ======================================================

    @staticmethod
    def get_courses(
        db: Session
    ):
        """
        Return all courses ordered by latest first.
        """

        return (
            db.query(Course)
            .order_by(Course.id.desc())
            .all()
        )


    # ======================================================
    # Get Course By ID
    # ======================================================

    @staticmethod
    def get_course(
        db: Session,
        course_id: int
    ):
        """
        Return a course with all modules and lessons.
        """

        return (
            db.query(Course)
            .options(
                joinedload(Course.modules)
                .joinedload(Module.lessons)
            )
            .filter(
                Course.id == course_id
            )
            .first()
        )


    # ======================================================
    # Update Course
    # ======================================================

    @staticmethod
    def update_course(
        db: Session,
        course_id: int,
        data: dict
    ):
        """
        Update course details.
        """

        course = (
            db.query(Course)
            .filter(
                Course.id == course_id
            )
            .first()
        )

        if not course:

            return None

        course.title = data["title"]

        course.description = data["description"]

        course.category = data["category"]

        course.level = data["level"]

        course.duration = data["duration"]

        course.price = data["price"]

        db.commit()

        db.refresh(course)

        return course


    # ======================================================
    # Create Module
    # ======================================================

    @staticmethod
    def create_module(
        db: Session,
        course_id: int,
        data: dict
    ):
        """
        Create a new module for a course.
        """

        # --------------------------------------------------
        # Check Course
        # --------------------------------------------------

        course = (
            db.query(Course)
            .filter(
                Course.id == course_id
            )
            .first()
        )

        if not course:

            return None


        # --------------------------------------------------
        # Find Last Module Order
        # --------------------------------------------------

        last_order = (
            db.query(
                func.max(
                    Module.display_order
                )
            )
            .filter(
                Module.course_id == course_id
            )
            .scalar()
        )


        # --------------------------------------------------
        # Calculate Next Order
        # --------------------------------------------------

        next_order = (

            last_order + 1

            if last_order is not None

            else 1

        )


        # --------------------------------------------------
        # Create Module
        # --------------------------------------------------

        module = Module(

            course_id=course_id,

            title=data["title"],

            description=data.get(
                "description"
            ),

            display_order=next_order,

            is_active=True

        )


        db.add(module)

        db.commit()

        db.refresh(module)

        return module

    # ======================================================
    # Update Module
    # ======================================================

    @staticmethod
    def update_module(
            db: Session,
            module_id: int,
            data: dict
    ):
        """
        Update module details.
        """

        module = (
            db.query(Module)
            .filter(
                Module.id == module_id
            )
            .first()
        )

        if not module:
            return None

        module.title = data["title"]

        module.description = data.get(
            "description"
        )

        db.commit()

        db.refresh(module)

        return module

    # ======================================================
    # Delete Module
    # ======================================================

    @staticmethod
    def delete_module(
            db: Session,
            module_id: int
    ):
        """
        Delete a module and its lessons.
        """

        module = (
            db.query(Module)
            .filter(
                Module.id == module_id
            )
            .first()
        )

        if not module:
            return None

        db.delete(module)

        db.commit()

        return module