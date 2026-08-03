"""
==========================================================
SkillForge LMS
AI Curriculum Service
==========================================================
"""

from sqlalchemy.orm import Session

from app.ai.manager import AIManager

from app.models.course import Course
from app.models.module import Module
from app.models.lesson import Lesson


class CurriculumService:
    """
    Curriculum Service
    """

    @staticmethod
    def generate(
        course_name: str,
        difficulty: str,
        duration: str,
        target_audience: str
    ):
        """
        Generate curriculum using configured AI provider.
        """

        provider = AIManager.get_provider()

        return provider.generate_curriculum(
            course_name=course_name,
            difficulty=difficulty,
            duration=duration,
            target_audience=target_audience
        )

    @staticmethod
    def save_curriculum(
        db: Session,
        curriculum: dict,
        difficulty: str,
        duration: int = 90
    ):
        """
        Save AI generated curriculum into database.
        """

        # ==================================================
        # Create Course
        # ==================================================

        course = Course(
            title=curriculum["course"],
            description=f"AI Generated Course - {curriculum['course']}",
            category="AI Generated",
            level=difficulty,
            duration=duration,
            price=0,
            is_active=False
        )

        db.add(course)
        db.flush()

        # ==================================================
        # Create Modules
        # ==================================================

        for module_index, module_data in enumerate(
            curriculum["modules"],
            start=1
        ):

            module = Module(
                course_id=course.id,
                title=module_data["title"],
                description=module_data.get("description"),
                display_order=module_index,
                is_active=True
            )

            db.add(module)
            db.flush()

            # ==============================================
            # Create Lessons
            # ==============================================

            for lesson_index, lesson_data in enumerate(
                module_data["lessons"],
                start=1
            ):

                lesson = Lesson(

                    module_id=module.id,

                    title=lesson_data["title"],

                    topic=lesson_data["title"],

                    keywords="",

                    difficulty=difficulty,

                    estimated_minutes=30,

                    display_order=lesson_index,

                    is_active=True

                )

                db.add(lesson)

        db.commit()

        db.refresh(course)

        return {
            "success": True,
            "course_id": course.id,
            "course_name": course.title,
            "message": "Curriculum saved successfully."
        }