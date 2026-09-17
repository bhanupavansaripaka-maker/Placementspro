"""
==========================================================
SkillForge LMS
Quiz Schemas
==========================================================
"""

from pydantic import BaseModel, Field, field_validator


# ==========================================================
# Generate Quiz Request
# ==========================================================

class QuizGenerateRequest(BaseModel):

    number_of_questions: int = Field(
        default=10,
        ge=1,
        le=50
    )


# ==========================================================
# Update Quiz Question Request
# ==========================================================

class QuizQuestionUpdateRequest(BaseModel):

    id: int | None = None

    question: str = Field(
        ...,
        min_length=1,
        max_length=1000
    )

    option_a: str = Field(
        ...,
        min_length=1,
        max_length=500
    )

    option_b: str = Field(
        ...,
        min_length=1,
        max_length=500
    )

    option_c: str = Field(
        ...,
        min_length=1,
        max_length=500
    )

    option_d: str = Field(
        ...,
        min_length=1,
        max_length=500
    )

    correct_answer: str = Field(
        ...,
        min_length=1,
        max_length=1
    )

    explanation: str | None = Field(
        default=None,
        max_length=2000
    )

    display_order: int = Field(
        default=1,
        ge=1
    )

    is_active: bool = True

    # ======================================================
    # Validate Correct Answer
    # ======================================================

    @field_validator("correct_answer")
    @classmethod
    def validate_correct_answer(
        cls,
        value: str
    ):

        value = value.upper().strip()

        if value not in {
            "A",
            "B",
            "C",
            "D"
        }:

            raise ValueError(
                "correct_answer must be A, B, C, or D."
            )

        return value


# ==========================================================
# Update Quiz Request
# ==========================================================

class QuizUpdateRequest(BaseModel):

    title: str = Field(
        ...,
        min_length=1,
        max_length=200
    )

    description: str | None = Field(
        default=None,
        max_length=1000
    )

    difficulty: str = Field(
        default="Beginner",
        min_length=1,
        max_length=30
    )

    passing_score: int = Field(
        default=60,
        ge=0,
        le=100
    )

    is_active: bool = True

    questions: list[
        QuizQuestionUpdateRequest
    ] = Field(
        default_factory=list
    )