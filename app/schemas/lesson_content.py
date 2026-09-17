"""
==========================================================
SkillForge LMS
Lesson Content Schemas
==========================================================
"""

from pydantic import BaseModel


# ==========================================================
# AI Lesson Content
# ==========================================================

class AILessonContent(BaseModel):
    """
    Structured AI generated lesson content.
    """

    explanation: str

    learning_objectives: list[str]

    examples: list[str]

    code_examples: list[str]

    practical_exercise: str

    key_points: list[str]


# ==========================================================
# Update Lesson Content Request
# ==========================================================

class UpdateLessonContentRequest(BaseModel):
    """
    Request used by Admin to manually edit
    generated lesson content.
    """

    explanation: str

    learning_objectives: list[str]

    examples: list[str]

    code_examples: list[str]

    practical_exercise: str

    key_points: list[str]