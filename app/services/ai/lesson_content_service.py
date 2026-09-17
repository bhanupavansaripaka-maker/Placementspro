"""
==========================================================
SkillForge LMS
Lesson Content Service
==========================================================
"""

from sqlalchemy.orm import Session

from app.ai.manager import AIManager

from app.models.lesson import Lesson
from app.models.lesson_content import LessonContent


class LessonContentService:
    """
    Service responsible for AI lesson content generation
    and persistence.
    """

    # ======================================================
    # Generate Lesson Content
    # ======================================================

    @staticmethod
    def generate(
        db: Session,
        lesson_id: int,
        target_audience: str = "Engineering Students"
    ):
        """
        Generate AI content for an existing lesson.
        """

        # ==================================================
        # Get Lesson
        # ==================================================

        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.id == lesson_id
            )
            .first()
        )

        if not lesson:

            return None


        # ==================================================
        # Get Module
        # ==================================================

        module = lesson.module

        if not module:

            raise ValueError(
                "Lesson module not found."
            )


        # ==================================================
        # Get Course
        # ==================================================

        course = module.course

        if not course:

            raise ValueError(
                "Lesson course not found."
            )


        # ==================================================
        # Get AI Provider
        # ==================================================

        provider = AIManager.get_provider()


        # ==================================================
        # Generate Content
        # ==================================================

        content = provider.generate_lesson(

            course_name=course.title,

            module_title=module.title,

            lesson_title=lesson.title,

            topic=lesson.topic,

            difficulty=lesson.difficulty,

            target_audience=target_audience

        )


        # ==================================================
        # Check Existing Content
        # ==================================================

        lesson_content = (
            db.query(LessonContent)
            .filter(
                LessonContent.lesson_id == lesson.id
            )
            .first()
        )


        if lesson_content:

            # ----------------------------------------------
            # Update Existing Content
            # ----------------------------------------------

            lesson_content.explanation = (
                content["explanation"]
            )

            lesson_content.learning_objectives = (
                "\n".join(
                    content["learning_objectives"]
                )
            )

            lesson_content.examples = (
                "\n".join(
                    content["examples"]
                )
            )

            lesson_content.code_examples = (
                "\n\n".join(
                    content["code_examples"]
                )
            )

            lesson_content.practical_exercise = (
                content["practical_exercise"]
            )

            lesson_content.key_points = (
                "\n".join(
                    content["key_points"]
                )

            )

        else:

            # ----------------------------------------------
            # Create New Content
            # ----------------------------------------------

            lesson_content = LessonContent(

                lesson_id=lesson.id,

                explanation=(
                    content["explanation"]
                ),

                learning_objectives=(
                    "\n".join(
                        content["learning_objectives"]
                    )
                ),

                examples=(
                    "\n".join(
                        content["examples"]
                    )
                ),

                code_examples=(
                    "\n\n".join(
                        content["code_examples"]
                    )
                ),

                practical_exercise=(
                    content["practical_exercise"]
                ),

                key_points=(
                    "\n".join(
                        content["key_points"]
                    )
                )

            )

            db.add(
                lesson_content
            )


        # ==================================================
        # Save
        # ==================================================

        db.commit()

        db.refresh(
            lesson_content
        )


        return lesson_content


    # ======================================================
    # Update Lesson Content
    # ======================================================

    @staticmethod
    def update_content(
        db: Session,
        lesson_id: int,
        data: dict
    ):
        """
        Update existing lesson content manually
        from the Admin interface.
        """

        # ==================================================
        # Find Lesson
        # ==================================================

        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.id == lesson_id
            )
            .first()
        )

        if not lesson:

            return None


        # ==================================================
        # Find Lesson Content
        # ==================================================

        lesson_content = (
            db.query(LessonContent)
            .filter(
                LessonContent.lesson_id == lesson_id
            )
            .first()
        )


        if not lesson_content:

            return None


        # ==================================================
        # Update Fields
        # ==================================================

        lesson_content.explanation = (
            data["explanation"]
        )

        lesson_content.learning_objectives = (
            "\n".join(
                data["learning_objectives"]
            )
        )

        lesson_content.examples = (
            "\n".join(
                data["examples"]
            )
        )

        lesson_content.code_examples = (
            "\n\n".join(
                data["code_examples"]
            )
        )

        lesson_content.practical_exercise = (
            data["practical_exercise"]
        )

        lesson_content.key_points = (
            "\n".join(
                data["key_points"]
            )
        )


        # ==================================================
        # Save Changes
        # ==================================================

        db.commit()

        db.refresh(
            lesson_content
        )


        return lesson_content