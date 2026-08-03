"""
==========================================================
SkillForge AI
AI Router
==========================================================
"""

from fastapi import APIRouter, HTTPException, status

from app.services.ai.curriculum_service import CurriculumService
from app.schemas.ai import (
    CurriculumGenerateRequest,
    CurriculumGenerateResponse
)

router = APIRouter(
    prefix="/api/ai",
    tags=["Artificial Intelligence"]
)


# ==========================================================
# Generate Curriculum
# ==========================================================

@router.post(
    "/generate-curriculum",
    response_model=CurriculumGenerateResponse
)
def generate_curriculum(
    request: CurriculumGenerateRequest
):
    """
    Generate AI Curriculum.
    """

    try:

        curriculum = CurriculumService.generate(
            course_name=request.course_name,
            difficulty=request.difficulty,
            duration=request.duration,
            target_audience=request.target_audience
        )

        return curriculum

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )