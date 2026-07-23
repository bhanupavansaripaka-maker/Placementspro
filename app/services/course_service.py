"""
==========================================================
SkillForge Platform
Course Service
==========================================================
"""

from sqlalchemy.orm import Session

from app.models.course import Course

from app.schemas.course import (
    CourseCreate,
    CourseUpdate
)


class CourseService:
    """
    Course Service
    """

    # ======================================================
    # Create Course
    # ======================================================

    @staticmethod
    def create(
        db: Session,
        course: CourseCreate
    ):
        """
        Create a new course.
        """

        new_course = Course(
            title=course.title,
            description=course.description,
            category=course.category,
            level=course.level,
            duration=course.duration,
            price=course.price
        )

        db.add(new_course)
        db.commit()
        db.refresh(new_course)

        return new_course

    # ======================================================
    # Get All Courses
    # ======================================================

    @staticmethod
    def get_all(
        db: Session
    ):
        """
        Return all courses.
        """

        return (
            db.query(Course)
            .order_by(Course.id.desc())
            .all()
        )

    # ======================================================
    # Get Active Courses
    # ======================================================

    @staticmethod
    def get_active(
        db: Session
    ):
        """
        Return only active courses.
        """

        return (
            db.query(Course)
            .filter(Course.is_active == True)
            .order_by(Course.id.desc())
            .all()
        )

    # ======================================================
    # Get Course By ID
    # ======================================================

    @staticmethod
    def get_by_id(
        db: Session,
        course_id: int
    ):
        """
        Return a single course.
        """

        return (
            db.query(Course)
            .filter(Course.id == course_id)
            .first()
        )

    # ======================================================
    # Update Course
    # ======================================================

    @staticmethod
    def update(
        db: Session,
        course_id: int,
        updated_course: CourseUpdate
    ):
        """
        Update a course.
        """

        course = CourseService.get_by_id(
            db,
            course_id
        )

        if course is None:
            return None

        update_data = updated_course.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(course, key, value)

        db.commit()
        db.refresh(course)

        return course

    # ======================================================
    # Delete Course
    # ======================================================

    @staticmethod
    def delete(
        db: Session,
        course_id: int
    ):
        """
        Delete a course.
        """

        course = CourseService.get_by_id(
            db,
            course_id
        )

        if course is None:
            return None

        db.delete(course)
        db.commit()

        return course