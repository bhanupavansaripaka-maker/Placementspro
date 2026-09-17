"""
==========================================================
SkillForge LMS
AI Quiz Service
==========================================================
"""

from sqlalchemy.orm import Session

from app.ai.manager import AIManager

from app.models.lesson import Lesson
from app.models.quiz import Quiz, QuizQuestion


class QuizService:
    """
    Service responsible for generating, saving,
    and updating AI-generated quizzes.
    """

    # ======================================================
    # Generate Quiz
    # ======================================================

    @staticmethod
    def generate(
        db: Session,
        lesson_id: int,
        number_of_questions: int = 10,
        target_audience: str = "Engineering Students"
    ):
        """
        Generate an AI quiz for an existing lesson
        and save it into the database.
        """

        # ==================================================
        # Validate Question Count
        # ==================================================

        if not 1 <= number_of_questions <= 30:

            raise ValueError(
                "Number of questions must be between 1 and 30."
            )

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
        # Generate Quiz Using AI
        # ==================================================

        quiz_data = provider.generate_quiz(

            course_name=course.title,

            module_title=module.title,

            lesson_title=lesson.title,

            topic=lesson.topic,

            difficulty=lesson.difficulty,

            number_of_questions=number_of_questions,

            target_audience=target_audience

        )

        # ==================================================
        # Check Existing Quiz
        # ==================================================

        quiz = (
            db.query(Quiz)
            .filter(
                Quiz.lesson_id == lesson.id
            )
            .first()
        )

        # ==================================================
        # Update Existing Quiz
        # ==================================================

        if quiz:

            quiz.title = quiz_data["title"]

            quiz.description = (
                quiz_data.get("description")
            )

            quiz.difficulty = (
                quiz_data.get(
                    "difficulty",
                    lesson.difficulty
                )
            )

            quiz.passing_score = (
                quiz_data.get(
                    "passing_score",
                    60
                )
            )

            quiz.is_active = True

            # ----------------------------------------------
            # Remove old questions
            # ----------------------------------------------

            quiz.questions.clear()

        # ==================================================
        # Create New Quiz
        # ==================================================

        else:

            quiz = Quiz(

                lesson_id=lesson.id,

                title=quiz_data["title"],

                description=(
                    quiz_data.get("description")
                ),

                difficulty=(
                    quiz_data.get(
                        "difficulty",
                        lesson.difficulty
                    )
                ),

                passing_score=(
                    quiz_data.get(
                        "passing_score",
                        60
                    )
                ),

                is_active=True

            )

            db.add(quiz)

            db.flush()

        # ==================================================
        # Create Questions
        # ==================================================

        for question_index, question_data in enumerate(
            quiz_data["questions"],
            start=1
        ):

            question = QuizQuestion(

                quiz_id=quiz.id,

                question=question_data["question"],

                option_a=question_data["option_a"],

                option_b=question_data["option_b"],

                option_c=question_data["option_c"],

                option_d=question_data["option_d"],

                correct_answer=(
                    question_data["correct_answer"]
                    .upper()
                    .strip()
                ),

                explanation=(
                    question_data.get(
                        "explanation"
                    )
                ),

                display_order=question_index,

                is_active=True

            )

            db.add(question)

        # ==================================================
        # Save Database Changes
        # ==================================================

        db.commit()

        db.refresh(quiz)

        return quiz

    # ======================================================
    # Update Existing Quiz
    # ======================================================

    @staticmethod
    def update(
        db: Session,
        lesson_id: int,
        data: dict
    ):
        """
        Update an existing quiz and its questions.

        Existing questions are updated using their IDs.

        Questions with id=None are created as new questions.

        Existing questions that are not included in the
        submitted request are deleted.
        """

        # ==================================================
        # Get Existing Quiz
        # ==================================================

        quiz = (
            db.query(Quiz)
            .filter(
                Quiz.lesson_id == lesson_id
            )
            .first()
        )

        if not quiz:

            return None

        # ==================================================
        # Update Quiz Information
        # ==================================================

        quiz.title = (
            data["title"]
        )

        quiz.description = (
            data.get("description")
        )

        quiz.difficulty = (
            data.get(
                "difficulty",
                quiz.difficulty
            )
        )

        quiz.passing_score = (
            data.get(
                "passing_score",
                quiz.passing_score
            )
        )

        quiz.is_active = (
            data.get(
                "is_active",
                quiz.is_active
            )
        )

        # ==================================================
        # Get Submitted Questions
        # ==================================================

        questions_data = data.get(
            "questions",
            []
        )

        # ==================================================
        # Existing Questions
        # ==================================================

        existing_questions = list(
            quiz.questions
        )

        existing_question_ids = {

            question.id

            for question in existing_questions

            if question.id is not None

        }

        submitted_question_ids = set()

        # ==================================================
        # Process Submitted Questions
        # ==================================================

        for question_index, question_data in enumerate(
            questions_data,
            start=1
        ):

            question_id = question_data.get(
                "id"
            )

            # ==================================================
            # Existing Question
            # ==================================================

            if question_id is not None:

                # ------------------------------------------
                # Make sure question belongs to this quiz
                # ------------------------------------------

                if question_id not in existing_question_ids:

                    raise ValueError(
                        "Question does not belong to this quiz."
                    )

                question = next(

                    (
                        item

                        for item in existing_questions

                        if item.id == question_id

                    ),

                    None

                )

                if not question:

                    raise ValueError(
                        f"Question {question_id} not found."
                    )

                submitted_question_ids.add(
                    question_id
                )

            # ==================================================
            # New Question
            # ==================================================

            else:

                question = QuizQuestion(
                    quiz_id=quiz.id
                )

                db.add(question)

            # ==================================================
            # Update Question Data
            # ==================================================

            question.question = (
                question_data["question"]
            )

            question.option_a = (
                question_data["option_a"]
            )

            question.option_b = (
                question_data["option_b"]
            )

            question.option_c = (
                question_data["option_c"]
            )

            question.option_d = (
                question_data["option_d"]
            )

            question.correct_answer = (
                question_data["correct_answer"]
                .upper()
                .strip()
            )

            question.explanation = (
                question_data.get(
                    "explanation"
                )
            )

            question.display_order = (
                question_index
            )

            question.is_active = (
                question_data.get(
                    "is_active",
                    True
                )
            )

        # ==================================================
        # Delete Removed Questions
        # ==================================================

        for question in existing_questions:

            if question.id not in submitted_question_ids:

                db.delete(
                    question
                )

        # ==================================================
        # Save Changes
        # ==================================================

        db.commit()

        db.refresh(quiz)

        return quiz