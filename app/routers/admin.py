"""
==========================================================
SkillForge LMS
Admin Router
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


# ==========================================================
# Models
# ==========================================================

from app.models.quiz import Quiz


# ==========================================================
# Schemas
# ==========================================================

from app.schemas.admin import (
    AdminDashboardStatistics,
    UpdateCourseRequest,
    CreateModuleRequest,
    UpdateModuleRequest
)

from app.schemas.ai import (
    CurriculumSaveRequest
)

from app.schemas.lesson_content import (
    UpdateLessonContentRequest
)

from app.schemas.quiz import (
    QuizGenerateRequest,
    QuizUpdateRequest
)


# ==========================================================
# Services
# ==========================================================

from app.services.admin_service import (
    AdminService
)

from app.services.ai.curriculum_service import (
    CurriculumService
)

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
    prefix="/admin",
    tags=["Admin"]
)

templates = Jinja2Templates(
    directory="app/templates"
)


# ==========================================================
# Admin Dashboard Page
# ==========================================================

@router.get(
    "/dashboard",
    response_class=HTMLResponse
)
def admin_dashboard(
    request: Request
):

    return templates.TemplateResponse(
        "admin/dashboard.html",
        {
            "request": request,
            "active_page": "dashboard"
        }
    )


# ==========================================================
# AI Course Builder Page
# ==========================================================

@router.get(
    "/ai-course-builder",
    response_class=HTMLResponse
)
def ai_course_builder(
    request: Request
):

    return templates.TemplateResponse(
        "admin/ai_course_builder.html",
        {
            "request": request,
            "active_page": "ai-course-builder"
        }
    )


# ==========================================================
# Dashboard Statistics API
# ==========================================================

@router.get(
    "/api/dashboard",
    response_model=AdminDashboardStatistics
)
def get_dashboard_statistics(
    db: Session = Depends(get_db)
):

    try:

        return AdminService.get_dashboard_statistics(db)

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ==========================================================
# Course Management Page
# ==========================================================

@router.get(
    "/courses",
    response_class=HTMLResponse
)
def courses_page(
    request: Request
):

    return templates.TemplateResponse(
        "admin/courses.html",
        {
            "request": request,
            "active_page": "courses"
        }
    )


# ==========================================================
# Get All Courses
# ==========================================================

@router.get(
    "/api/courses"
)
def get_courses(
    db: Session = Depends(get_db)
):

    courses = AdminService.get_courses(db)

    return [

        {
            "id": course.id,
            "title": course.title,
            "category": course.category,
            "level": course.level,
            "duration": course.duration,
            "price": course.price,
            "is_active": course.is_active
        }

        for course in courses

    ]


# ==========================================================
# Course Details Page
# ==========================================================

@router.get(
    "/course/{course_id}",
    response_class=HTMLResponse
)
def course_detail_page(
    request: Request,
    course_id: int
):

    return templates.TemplateResponse(
        "admin/course_detail.html",
        {
            "request": request,
            "course_id": course_id,
            "active_page": "courses"
        }
    )


# ==========================================================
# Get Course Details API
# ==========================================================

@router.get(
    "/api/course/{course_id}"
)
def get_course(
    course_id: int,
    db: Session = Depends(get_db)
):

    course = AdminService.get_course(
        db=db,
        course_id=course_id
    )

    if not course:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found."
        )

    return {

        "id": course.id,

        "title": course.title,

        "description": course.description,

        "category": course.category,

        "level": course.level,

        "duration": course.duration,

        "price": course.price,

        "is_active": course.is_active,

        "modules": [

            {

                "id": module.id,

                "title": module.title,

                "description": module.description,

                "display_order":
                    module.display_order,

                "is_active":
                    module.is_active,

                "lessons": [

                    {

                        "id": lesson.id,

                        "title": lesson.title,

                        "topic": lesson.topic,

                        "difficulty":
                            lesson.difficulty,

                        "estimated_minutes":
                            lesson.estimated_minutes,

                        # ==================================
                        # AI Lesson Content
                        # ==================================

                        "has_content":
                            lesson.content is not None,

                        "content": {

                            "id":
                                lesson.content.id,

                            "explanation":
                                lesson.content.explanation,

                            "learning_objectives":
                                lesson.content.learning_objectives,

                            "examples":
                                lesson.content.examples,

                            "code_examples":
                                lesson.content.code_examples,

                            "practical_exercise":
                                lesson.content.practical_exercise,

                            "key_points":
                                lesson.content.key_points

                        } if lesson.content else None,

                        # ==================================
                        # AI Quiz
                        # ==================================

                        "has_quiz":
                            lesson.quiz is not None,

                        "quiz": {

                            "id":
                                lesson.quiz.id,

                            "title":
                                lesson.quiz.title,

                            "description":
                                lesson.quiz.description,

                            "difficulty":
                                lesson.quiz.difficulty,

                            "passing_score":
                                lesson.quiz.passing_score,

                            "question_count":
                                len(
                                    lesson.quiz.questions
                                ),

                            "is_active":
                                lesson.quiz.is_active

                        } if lesson.quiz else None

                    }

                    for lesson in module.lessons

                ]

            }

            for module in course.modules

        ]

    }


# ==========================================================
# Update Course
# ==========================================================

@router.put(
    "/api/course/{course_id}"
)
def update_course(
    course_id: int,
    request: UpdateCourseRequest,
    db: Session = Depends(get_db)
):

    try:

        course = AdminService.update_course(
            db=db,
            course_id=course_id,
            data=request.model_dump()
        )

        if not course:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found."
            )

        return {

            "success": True,

            "message":
                "Course updated successfully."

        }

    except HTTPException:

        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ==========================================================
# Publish / Unpublish Course
# ==========================================================

@router.put(
    "/api/course/{course_id}/status"
)
def update_course_status(
    course_id: int,
    db: Session = Depends(get_db)
):

    try:

        course = AdminService.get_course(
            db=db,
            course_id=course_id
        )

        if not course:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found."
            )

        # --------------------------------------------------
        # Toggle Course Status
        # --------------------------------------------------

        course.is_active = not course.is_active

        # --------------------------------------------------
        # Save Changes
        # --------------------------------------------------

        db.commit()

        db.refresh(course)

        return {

            "success": True,

            "message": (
                "Course published successfully."
                if course.is_active
                else "Course unpublished successfully."
            ),

            "course_id":
                course.id,

            "is_active":
                course.is_active

        }

    except HTTPException:

        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ==========================================================
# Create Module
# ==========================================================

@router.post(
    "/api/course/{course_id}/modules"
)
def create_module(
    course_id: int,
    request: CreateModuleRequest,
    db: Session = Depends(get_db)
):

    try:

        module = AdminService.create_module(
            db=db,
            course_id=course_id,
            data=request.model_dump()
        )

        if not module:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found."
            )

        return {

            "success": True,

            "message":
                "Module created successfully.",

            "module": {

                "id":
                    module.id,

                "course_id":
                    module.course_id,

                "title":
                    module.title,

                "description":
                    module.description,

                "display_order":
                    module.display_order,

                "is_active":
                    module.is_active

            }

        }

    except HTTPException:

        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ==========================================================
# Update Module
# ==========================================================

@router.put(
    "/api/module/{module_id}"
)
def update_module(
    module_id: int,
    request: UpdateModuleRequest,
    db: Session = Depends(get_db)
):

    try:

        module = AdminService.update_module(
            db=db,
            module_id=module_id,
            data=request.model_dump()
        )

        if not module:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Module not found."
            )

        return {

            "success": True,

            "message":
                "Module updated successfully.",

            "module": {

                "id":
                    module.id,

                "course_id":
                    module.course_id,

                "title":
                    module.title,

                "description":
                    module.description,

                "display_order":
                    module.display_order,

                "is_active":
                    module.is_active

            }

        }

    except HTTPException:

        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ==========================================================
# Delete Module
# ==========================================================

@router.delete(
    "/api/module/{module_id}"
)
def delete_module(
    module_id: int,
    db: Session = Depends(get_db)
):

    try:

        module = AdminService.delete_module(
            db=db,
            module_id=module_id
        )

        if not module:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Module not found."
            )

        return {

            "success": True,

            "message":
                "Module deleted successfully.",

            "module_id":
                module_id

        }

    except HTTPException:

        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ==========================================================
# Save AI Curriculum
# ==========================================================

@router.post(
    "/api/save-curriculum"
)
def save_curriculum(
    request: CurriculumSaveRequest,
    db: Session = Depends(get_db)
):

    try:

        result = CurriculumService.save_curriculum(
            db=db,
            curriculum=request.curriculum,
            difficulty=request.difficulty,
            duration=request.duration
        )

        return result

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ==========================================================
# Generate AI Lesson Content
# ==========================================================

@router.post(
    "/api/lesson/{lesson_id}/generate-content"
)
def generate_lesson_content(
    lesson_id: int,
    db: Session = Depends(get_db)
):

    try:

        content = LessonContentService.generate(
            db=db,
            lesson_id=lesson_id
        )

        if not content:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson not found."
            )

        return {

            "success": True,

            "message":
                "Lesson content generated successfully.",

            "lesson_id":
                content.lesson_id,

            "content": {

                "id":
                    content.id,

                "explanation":
                    content.explanation,

                "learning_objectives":
                    content.learning_objectives,

                "examples":
                    content.examples,

                "code_examples":
                    content.code_examples,

                "practical_exercise":
                    content.practical_exercise,

                "key_points":
                    content.key_points

            }

        }

    except HTTPException:

        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ==========================================================
# Update Lesson Content
# ==========================================================

@router.put(
    "/api/lesson/{lesson_id}/content"
)
def update_lesson_content(
    lesson_id: int,
    request: UpdateLessonContentRequest,
    db: Session = Depends(get_db)
):

    try:

        content = LessonContentService.update_content(
            db=db,
            lesson_id=lesson_id,
            data=request.model_dump()
        )

        if not content:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson content not found."
            )

        return {

            "success": True,

            "message":
                "Lesson content updated successfully.",

            "lesson_id":
                content.lesson_id,

            "content": {

                "id":
                    content.id,

                "explanation":
                    content.explanation,

                "learning_objectives":
                    content.learning_objectives,

                "examples":
                    content.examples,

                "code_examples":
                    content.code_examples,

                "practical_exercise":
                    content.practical_exercise,

                "key_points":
                    content.key_points

            }

        }

    except HTTPException:

        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ==========================================================
# Generate AI Quiz
# ==========================================================

@router.post(
    "/api/lesson/{lesson_id}/generate-quiz"
)
def generate_quiz(
    lesson_id: int,
    request: QuizGenerateRequest,
    db: Session = Depends(get_db)
):

    try:

        quiz = QuizService.generate(
            db=db,
            lesson_id=lesson_id,
            number_of_questions=
                request.number_of_questions
        )

        if not quiz:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson not found."
            )

        return {

            "success": True,

            "message":
                "Quiz generated successfully.",

            "quiz": {

                "id":
                    quiz.id,

                "lesson_id":
                    quiz.lesson_id,

                "title":
                    quiz.title,

                "description":
                    quiz.description,

                "difficulty":
                    quiz.difficulty,

                "passing_score":
                    quiz.passing_score,

                "questions": [

                    {

                        "id":
                            question.id,

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

                        "correct_answer":
                            question.correct_answer,

                        "explanation":
                            question.explanation,

                        "display_order":
                            question.display_order,

                        "is_active":
                            question.is_active

                    }

                    for question in quiz.questions

                ]

            }

        }

    except HTTPException:

        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ==========================================================
# Update Saved AI Quiz
# ==========================================================

@router.put(
    "/api/lesson/{lesson_id}/quiz"
)
def update_lesson_quiz(
    lesson_id: int,
    request: QuizUpdateRequest,
    db: Session = Depends(get_db)
):

    try:

        quiz = QuizService.update(
            db=db,
            lesson_id=lesson_id,
            data=request.model_dump()
        )

        if not quiz:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz not found for this lesson."
            )

        return {

            "success": True,

            "message":
                "Quiz updated successfully.",

            "quiz": {

                "id":
                    quiz.id,

                "lesson_id":
                    quiz.lesson_id,

                "title":
                    quiz.title,

                "description":
                    quiz.description,

                "difficulty":
                    quiz.difficulty,

                "passing_score":
                    quiz.passing_score,

                "is_active":
                    quiz.is_active,

                "questions": [

                    {

                        "id":
                            question.id,

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

                        "correct_answer":
                            question.correct_answer,

                        "explanation":
                            question.explanation,

                        "display_order":
                            question.display_order,

                        "is_active":
                            question.is_active

                    }

                    for question in quiz.questions

                ]

            }

        }

    except HTTPException:

        raise

    except ValueError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ==========================================================
# Get Saved Quiz
# ==========================================================

@router.get(
    "/api/lesson/{lesson_id}/quiz"
)
def get_lesson_quiz(
    lesson_id: int,
    db: Session = Depends(get_db)
):

    try:

        quiz = (
            db.query(Quiz)
            .filter(
                Quiz.lesson_id == lesson_id
            )
            .first()
        )

        if not quiz:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz not found for this lesson."
            )

        return {

            "success": True,

            "quiz": {

                "id":
                    quiz.id,

                "lesson_id":
                    quiz.lesson_id,

                "title":
                    quiz.title,

                "description":
                    quiz.description,

                "difficulty":
                    quiz.difficulty,

                "passing_score":
                    quiz.passing_score,

                "is_active":
                    quiz.is_active,

                "questions": [

                    {

                        "id":
                            question.id,

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

                        "correct_answer":
                            question.correct_answer,

                        "explanation":
                            question.explanation,

                        "display_order":
                            question.display_order,

                        "is_active":
                            question.is_active

                    }

                    for question in quiz.questions

                ]

            }

        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )