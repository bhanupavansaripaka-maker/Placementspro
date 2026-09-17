"""
==========================================================
SkillForge LMS
Curriculum Service
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
    Handles AI curriculum generation
    and database persistence.
    """

    # ======================================================
    # Generate Curriculum
    # ======================================================

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


    # ======================================================
    # Save AI Curriculum
    # ======================================================

    @staticmethod
    def save_curriculum(
        db: Session,
        curriculum,
        difficulty: str,
        duration: int = 90
    ):
        """
        Save AI generated curriculum into database.

        Structure:

        Course
            ↓
        Modules
            ↓
        Lessons
        """

        try:

            # ==================================================
            # Create Course
            # ==================================================

            course = Course(

                title=curriculum.course,

                description=(
                    f"AI Generated Course - "
                    f"{curriculum.course}"
                ),

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
                curriculum.modules,
                start=1
            ):

                module = Module(

                    course_id=course.id,

                    title=module_data.title,

                    description=module_data.description,

                    display_order=module_index,

                    is_active=True

                )

                db.add(module)

                db.flush()


                # ==============================================
                # Create Lessons
                # ==============================================

                for lesson_index, lesson_data in enumerate(
                    module_data.lessons,
                    start=1
                ):

                    # ------------------------------------------
                    # Convert keywords list to database string
                    # ------------------------------------------

                    keywords = ", ".join(
                        lesson_data.keywords
                    )


                    lesson = Lesson(

                        module_id=module.id,

                        title=lesson_data.title,

                        topic=lesson_data.topic,

                        keywords=keywords,

                        difficulty=lesson_data.difficulty,

                        estimated_minutes=(
                            lesson_data.estimated_minutes
                        ),

                        display_order=lesson_index,

                        is_active=True

                    )

                    db.add(lesson)


            # ==================================================
            # Commit Curriculum
            # ==================================================

            db.commit()

            db.refresh(course)


            # ==================================================
            # Return Result
            # ==================================================

            return {

                "success": True,

                "course_id": course.id,

                "course_name": course.title,

                "message":
                    "Curriculum saved successfully."

            }


        except Exception:

            db.rollback()

            raise