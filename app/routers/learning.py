"""
==========================================================
SkillForge LMS
Learning Router
==========================================================
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status
)

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.course import Course
from app.models.lesson import Lesson
from app.models.lesson_content import LessonContent
from app.models.quiz import Quiz

from app.services.course_service import CourseService

from app.services.ai.lesson_content_service import (
    LessonContentService
)

from app.services.ai.quiz_service import (
    QuizService
)


# ==========================================================
# Router
# ==========================================================

router = APIRouter(
    tags=["Learning"]
)


# ==========================================================
# Templates
# ==========================================================

templates = Jinja2Templates(
    directory="app/templates"
)


# ==========================================================
# Learning Player Page
# ==========================================================

@router.get(
    "/learn/{course_id}",
    response_class=HTMLResponse
)
def learning_page(
    request: Request,
    course_id: int,
    db: Session = Depends(get_db)
):
    """
    Render the student learning player.
    """

    # ======================================================
    # Get Course
    # ======================================================

    course = CourseService.get_by_id(
        db=db,
        course_id=course_id
    )

    # ======================================================
    # Course Not Found
    # ======================================================

    if not course:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found."
        )

    # ======================================================
    # Course Inactive
    # ======================================================

    if not course.is_active:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course is not available."
        )

    # ======================================================
    # Render Learning Page
    # ======================================================

    return templates.TemplateResponse(
        "student/learning.html",
        {
            "request": request,
            "title": course.title,
            "active_page": "learning",
            "course_id": course.id
        }
    )


# ==========================================================
# Get Learning Course Data
# ==========================================================

@router.get(
    "/api/learning/course/{course_id}"
)
def get_learning_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    """
    Return course with modules and lessons
    for the learning player.
    """

    # ======================================================
    # Get Course
    # ======================================================

    course = (
        db.query(Course)
        .filter(
            Course.id == course_id,
            Course.is_active == True
        )
        .first()
    )

    # ======================================================
    # Course Not Found
    # ======================================================

    if not course:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found."
        )

    # ======================================================
    # Build Modules
    # ======================================================

    modules_data = []

    for module in course.modules:

        # --------------------------------------------------
        # Skip Inactive Modules
        # --------------------------------------------------

        if not module.is_active:

            continue

        lessons_data = []

        # --------------------------------------------------
        # Build Lessons
        # --------------------------------------------------

        for lesson in module.lessons:

            # Skip Inactive Lessons

            if not lesson.is_active:

                continue

            lessons_data.append(
                {
                    "id": lesson.id,

                    "title": lesson.title,

                    "topic": lesson.topic,

                    "keywords": lesson.keywords,

                    "difficulty": lesson.difficulty,

                    "estimated_minutes":
                        lesson.estimated_minutes,

                    "display_order":
                        lesson.display_order
                }
            )

        # --------------------------------------------------
        # Add Module
        # --------------------------------------------------

        modules_data.append(
            {
                "id": module.id,

                "title": module.title,

                "description": module.description,

                "display_order":
                    module.display_order,

                "lessons": lessons_data
            }
        )

    # ======================================================
    # Return Learning Data
    # ======================================================

    return {

        "id": course.id,

        "title": course.title,

        "description": course.description,

        "category": course.category,

        "level": course.level,

        "duration": course.duration,

        "price": course.price,

        "modules": modules_data

    }


# ==========================================================
# Get / Generate Lesson Content
# ==========================================================

@router.get(
    "/api/learning/lesson/{lesson_id}"
)
def get_lesson_content(
    lesson_id: int,
    db: Session = Depends(get_db)
):
    """
    Return AI-generated lesson content.

    If lesson content does not already exist,
    generate it using AI and save it.
    """

    # ======================================================
    # Get Lesson
    # ======================================================

    lesson = (
        db.query(Lesson)
        .filter(
            Lesson.id == lesson_id,
            Lesson.is_active == True
        )
        .first()
    )

    # ======================================================
    # Lesson Not Found
    # ======================================================

    if not lesson:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found."
        )

    # ======================================================
    # Check Existing Content
    # ======================================================

    lesson_content = (
        db.query(LessonContent)
        .filter(
            LessonContent.lesson_id == lesson_id
        )
        .first()
    )

    # ======================================================
    # Generate Content If Missing
    # ======================================================

    if not lesson_content:

        try:

            lesson_content = (
                LessonContentService.generate(
                    db=db,
                    lesson_id=lesson_id
                )
            )

        except Exception as e:

            raise HTTPException(
                status_code=(
                    status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=(
                    "Unable to generate lesson content: "
                    f"{str(e)}"
                )
            )

    # ======================================================
    # Generation Failed
    # ======================================================

    if not lesson_content:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "Lesson content could not be generated."
            )
        )

    # ======================================================
    # Return Lesson Content
    # ======================================================

    return {

        "lesson_id": lesson.id,

        "lesson_title": lesson.title,

        "topic": lesson.topic,

        "difficulty": lesson.difficulty,

        "estimated_minutes":
            lesson.estimated_minutes,

        "explanation":
            lesson_content.explanation,

        "learning_objectives":
            lesson_content.learning_objectives,

        "examples":
            lesson_content.examples,

        "code_examples":
            lesson_content.code_examples,

        "practical_exercise":
            lesson_content.practical_exercise,

        "key_points":
            lesson_content.key_points

    }


# ==========================================================
# Get / Generate Lesson Quiz
# ==========================================================

@router.get(
    "/api/learning/lesson/{lesson_id}/quiz"
)
def get_lesson_quiz(
    lesson_id: int,
    number_of_questions: int = 10,
    db: Session = Depends(get_db)
):
    """
    Return the quiz for a lesson.

    If a quiz does not exist,
    generate the quiz using AI.
    """

    # ======================================================
    # Validate Question Count
    # ======================================================

    if not 1 <= number_of_questions <= 30:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Number of questions must be "
                "between 1 and 30."
            )
        )

    # ======================================================
    # Get Lesson
    # ======================================================

    lesson = (
        db.query(Lesson)
        .filter(
            Lesson.id == lesson_id,
            Lesson.is_active == True
        )
        .first()
    )

    # ======================================================
    # Lesson Not Found
    # ======================================================

    if not lesson:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found."
        )

    # ======================================================
    # Check Existing Quiz
    # ======================================================

    quiz = (
        db.query(Quiz)
        .filter(
            Quiz.lesson_id == lesson_id,
            Quiz.is_active == True
        )
        .first()
    )

    # ======================================================
    # Generate Quiz If Missing
    # ======================================================

    if not quiz:

        try:

            quiz = QuizService.generate(
                db=db,
                lesson_id=lesson_id,
                number_of_questions=number_of_questions
            )

        except Exception as e:

            raise HTTPException(
                status_code=(
                    status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
                detail=(
                    "Unable to generate quiz: "
                    f"{str(e)}"
                )
            )

    # ======================================================
    # Quiz Generation Failed
    # ======================================================

    if not quiz:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "Quiz could not be generated."
            )
        )

    # ======================================================
    # Build Questions
    # ======================================================

    questions = []

    for question in quiz.questions:

        # Skip inactive questions

        if not question.is_active:

            continue

        questions.append(
            {
                "id": question.id,

                "question":
                    question.question,

                "option_a":
                    question.option_a,

                "option_b":
                    question.option_b,

                "option_c":
                    question.option_c,

                "option_d":
                    question.option_d,

                "display_order":
                    question.display_order
            }
        )

    # ======================================================
    # Return Quiz
    # ======================================================

    return {

        "quiz_id": quiz.id,

        "lesson_id": lesson.id,

        "title": quiz.title,

        "description":
            quiz.description,

        "difficulty":
            quiz.difficulty,

        "passing_score":
            quiz.passing_score,

        "questions":
            questions

    }


# ==========================================================
# Submit Quiz
# ==========================================================

@router.post(
    "/api/learning/quiz/{quiz_id}/submit"
)
def submit_quiz(
    quiz_id: int,
    submission: dict,
    db: Session = Depends(get_db)
):
    """
    Submit quiz answers and calculate results.
    """

    # ======================================================
    # Get Quiz
    # ======================================================

    quiz = (
        db.query(Quiz)
        .filter(
            Quiz.id == quiz_id,
            Quiz.is_active == True
        )
        .first()
    )

    # ======================================================
    # Quiz Not Found
    # ======================================================

    if not quiz:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found."
        )

    # ======================================================
    # Get Submitted Answers
    # ======================================================

    answers = submission.get(
        "answers",
        []
    )

    # ======================================================
    # Validate Answers
    # ======================================================

    if not answers:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No answers submitted."
        )

    # ======================================================
    # Build Submitted Answers Map
    # ======================================================

    submitted_answers = {}

    for answer in answers:

        question_id = answer.get(
            "question_id"
        )

        selected_answer = answer.get(
            "answer"
        )

        if (
            question_id is not None
            and selected_answer
        ):

            submitted_answers[
                question_id
            ] = (
                str(selected_answer)
                .upper()
                .strip()
            )

    # ======================================================
    # Get Active Questions
    # ======================================================

    active_questions = [

        question

        for question in quiz.questions

        if question.is_active

    ]

    # ======================================================
    # No Questions Available
    # ======================================================

    if not active_questions:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This quiz has no active questions."
        )

    # ======================================================
    # Calculate Result
    # ======================================================

    correct_count = 0

    wrong_count = 0

    unanswered_count = 0

    results = []

    for question in active_questions:

        selected_answer = (
            submitted_answers.get(
                question.id
            )
        )

        correct_answer = (
            question.correct_answer
            .upper()
            .strip()
        )

        # --------------------------------------------------
        # Unanswered Question
        # --------------------------------------------------

        if not selected_answer:

            unanswered_count += 1

            is_correct = False

        # --------------------------------------------------
        # Correct Answer
        # --------------------------------------------------

        elif selected_answer == correct_answer:

            correct_count += 1

            is_correct = True

        # --------------------------------------------------
        # Wrong Answer
        # --------------------------------------------------

        else:

            wrong_count += 1

            is_correct = False

        # --------------------------------------------------
        # Store Question Result
        # --------------------------------------------------

        results.append(
            {
                "question_id":
                    question.id,

                "question":
                    question.question,

                "selected_answer":
                    selected_answer,

                "correct_answer":
                    correct_answer,

                "is_correct":
                    is_correct,

                "explanation":
                    question.explanation
            }
        )

    # ======================================================
    # Calculate Score
    # ======================================================

    total_questions = len(
        active_questions
    )

    score = round(

        (
            correct_count
            / total_questions
        )
        * 100,

        2

    )

    # ======================================================
    # Determine Pass / Fail
    # ======================================================

    passed = (

        score >= quiz.passing_score

    )

    # ======================================================
    # Return Quiz Result
    # ======================================================

    return {

        "quiz_id":
            quiz.id,

        "total_questions":
            total_questions,

        "correct_answers":
            correct_count,

        "wrong_answers":
            wrong_count,

        "unanswered_questions":
            unanswered_count,

        "score":
            score,

        "passing_score":
            quiz.passing_score,

        "passed":
            passed,

        "results":
            results

    }