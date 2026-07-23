"""
==========================================================
SkillForge Platform
Enrollment Service
==========================================================
"""

from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.models.course import Course
from app.models.student import Student


class EnrollmentService:
    """
    Enrollment Service
    """

    # ======================================================
    # Enroll Student
    # ======================================================

    @staticmethod
    def enroll(
        db: Session,
        student_id: int,
        course_id: int
    ):
        """
        Enroll a student into a course.
        """

        student = (
            db.query(Student)
            .filter(Student.id == student_id)
            .first()
        )

        if student is None:
            return None

        course = (
            db.query(Course)
            .filter(Course.id == course_id)
            .first()
        )

        if course is None:
            return None

        existing = (
            db.query(Enrollment)
            .filter(
                Enrollment.student_id == student_id,
                Enrollment.course_id == course_id
            )
            .first()
        )

        if existing:
            return existing

        enrollment = Enrollment(
            student_id=student_id,
            course_id=course_id
        )

        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)

        return enrollment

    # ======================================================
    # Get Student Courses
    # ======================================================

    @staticmethod
    def get_student_courses(
        db: Session,
        student_id: int
    ):
        """
        Return all enrolled courses for a student.
        """

        enrollments = (
            db.query(Enrollment)
            .filter(
                Enrollment.student_id == student_id
            )
            .all()
        )

        result = []

        for enrollment in enrollments:

            result.append({
                "course_id": enrollment.course.id,
                "title": enrollment.course.title,
                "description": enrollment.course.description,
                "category": enrollment.course.category,
                "level": enrollment.course.level,
                "duration": enrollment.course.duration,
                "price": enrollment.course.price,
                "enrolled_at": enrollment.enrolled_at
            })

        return result