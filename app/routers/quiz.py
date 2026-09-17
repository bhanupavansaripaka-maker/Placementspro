"""
==========================================================
SkillForge LMS
Quiz Router
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

from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.student import Student
from app.models.quiz_attempt import QuizAttempt
from app.models.user import User

from app.services.ai.quiz_service import QuizService

from app.core.security import get_current_user


# ==========================================================
# Router
# ==========================================================

router = APIRouter(
    tags=["Quiz"]
)


# ==========================================================
# Templates
# ==========================================================

templates = Jinja2Templates(
    directory="app/templates"
)


# ==========================================================
# Quiz Page
# ==========================================================

@router.get(
    "/quiz/{lesson_id}",
    response_class=HTMLResponse
)
def quiz_page(
    request: Request,
    lesson_id: int,
    db: Session = Depends(get_db)
):
    """
    Render the student quiz page.

    If a quiz does not already exist for the lesson,
    generate it using AI.
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

    if not lesson:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found."
        )

    # ======================================================
    # Get Existing Quiz
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
    # Generate Quiz If It Does Not Exist
    # ======================================================

    if not quiz:

        try:

            quiz = QuizService.generate(
                db=db,
                lesson_id=lesson_id,
                number_of_questions=10
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
            detail="Quiz could not be generated."
        )

    # ======================================================
    # Render Quiz Page
    # ======================================================

    return templates.TemplateResponse(
        "student/quiz.html",
        {
            "request": request,
            "lesson_id": lesson_id,
            "quiz_id": quiz.id,
            "lesson_title": lesson.title,
            "active_page": "learning"
        }
    )


# ==========================================================
# Get Quiz
# ==========================================================

@router.get(
    "/api/quiz/lesson/{lesson_id}"
)
def get_quiz(
    lesson_id: int,
    db: Session = Depends(get_db)
):
    """
    Return quiz and questions for a lesson.

    If the quiz does not exist, generate it using AI.
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

    if not lesson:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found."
        )

    # ======================================================
    # Get Existing Quiz
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
    # Generate Quiz If Required
    # ======================================================

    if not quiz:

        try:

            quiz = QuizService.generate(
                db=db,
                lesson_id=lesson_id,
                number_of_questions=10
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
            detail="Quiz could not be generated."
        )

    # ======================================================
    # Build Questions
    # ======================================================

    questions = []

    for question in quiz.questions:

        if not question.is_active:

            continue

        questions.append(
            {
                "id": question.id,

                "question": question.question,

                "option_a": question.option_a,

                "option_b": question.option_b,

                "option_c": question.option_c,

                "option_d": question.option_d,

                "display_order":
                    question.display_order
            }
        )

    # ======================================================
    # Return Quiz
    # ======================================================

    return {

        "id": quiz.id,

        "lesson_id": quiz.lesson_id,

        "title": quiz.title,

        "description": quiz.description,

        "difficulty": quiz.difficulty,

        "passing_score": quiz.passing_score,

        "questions": questions

    }


# ==========================================================
# Submit Quiz
# ==========================================================

@router.post(
    "/api/quiz/{quiz_id}/submit"
)
def submit_quiz(
    quiz_id: int,
    answers: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit quiz answers, calculate the score,
    and save the quiz attempt for the student.
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

    if not quiz:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found."
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
    # Get Student
    # ======================================================

    student = (
        db.query(Student)
        .filter(
            Student.user_id == current_user.id
        )
        .first()
    )

    # ======================================================
    # Student Profile Not Found
    # ======================================================

    if not student:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found."
        )

    # ======================================================
    # Calculate Result
    # ======================================================

    active_questions = [

        question

        for question in quiz.questions

        if question.is_active

    ]

    total_questions = len(
        active_questions
    )

    correct_answers = 0

    results = []

    # ======================================================
    # Check Each Answer
    # ======================================================

    for question in active_questions:

        submitted_answer = answers.get(
            str(question.id)
        )

        correct_answer = (
            question.correct_answer
            .upper()
            .strip()
        )

        is_correct = (
            submitted_answer is not None
            and str(submitted_answer)
            .upper()
            .strip()
            == correct_answer
        )

        if is_correct:

            correct_answers += 1

        results.append(
            {
                "question_id":
                    question.id,

                "question":
                    question.question,

                "submitted_answer":
                    submitted_answer,

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

    if total_questions > 0:

        score = round(
            (
                correct_answers
                / total_questions
            ) * 100
        )

    else:

        score = 0

    # ======================================================
    # Pass / Fail
    # ======================================================

    passed = (
        score >= quiz.passing_score
    )

    # ======================================================
    # Save Quiz Attempt
    # ======================================================

    attempt = QuizAttempt(

        student_id=student.id,

        quiz_id=quiz.id,

        total_questions=total_questions,

        correct_answers=correct_answers,

        score=score,

        passed=passed

    )

    db.add(attempt)

    db.commit()

    db.refresh(attempt)

    # ======================================================
    # Return Result
    # ======================================================

    return {

        "attempt_id":
            attempt.id,

        "quiz_id":
            quiz.id,

        "quiz_title":
            quiz.title,

        "total_questions":
            total_questions,

        "correct_answers":
            correct_answers,

        "score":
            score,

        "passing_score":
            quiz.passing_score,

        "passed":
            passed,

        "results":
            results

    }