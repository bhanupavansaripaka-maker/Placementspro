"""
==========================================================
SkillForge LMS
AI Schemas
==========================================================
"""

from typing import Any

from pydantic import BaseModel


# ==========================================================
# Generate Curriculum Request
# ==========================================================

class CurriculumGenerateRequest(BaseModel):

    course_name: str

    difficulty: str

    duration: str

    target_audience: str


# ==========================================================
# Generate Curriculum Response
# ==========================================================

class CurriculumGenerateResponse(BaseModel):

    course: str

    modules: list[dict[str, Any]]


# ==========================================================
# Save Curriculum Request
# ==========================================================

class CurriculumSaveRequest(BaseModel):

    curriculum: dict[str, Any]

    difficulty: str

    duration: int = 90


# ==========================================================
# Save Curriculum Response
# ==========================================================

class CurriculumSaveResponse(BaseModel):

    success: bool

    course_id: int

    course_name: str

    message: str