"""
==========================================================
SkillForge LMS
AI Schemas
==========================================================
"""

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
# AI Generated Lesson
# ==========================================================

class AILesson(BaseModel):

    title: str

    topic: str

    keywords: list[str]

    difficulty: str

    estimated_minutes: int


# ==========================================================
# AI Generated Module
# ==========================================================

class AIModule(BaseModel):

    title: str

    description: str

    lessons: list[AILesson]


# ==========================================================
# AI Generated Curriculum
# ==========================================================

class AICurriculum(BaseModel):

    course: str

    modules: list[AIModule]


# ==========================================================
# Generate Curriculum Response
# ==========================================================

class CurriculumGenerateResponse(BaseModel):

    course: str

    modules: list[AIModule]


# ==========================================================
# Save Curriculum Request
# ==========================================================

class CurriculumSaveRequest(BaseModel):

    curriculum: AICurriculum

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