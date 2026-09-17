"""
==========================================================
SkillForge LMS
Quiz Attempt Model
==========================================================
"""

from datetime import datetime

from sqlalchemy import (
    Integer,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy.sql import func

from app.core.database import Base


# ==========================================================
# Quiz Attempt
# ==========================================================

class QuizAttempt(Base):
    """
    Stores a student's attempt at a quiz.
    """

    __tablename__ = "quiz_attempts"

    # ======================================================
    # Columns
    # ======================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id"),
        nullable=False,
        index=True
    )

    quiz_id: Mapped[int] = mapped_column(
        ForeignKey("quizzes.id"),
        nullable=False,
        index=True
    )

    total_questions: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    correct_answers: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    passed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    attempted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # ======================================================
    # Relationships
    # ======================================================

    student = relationship(
        "Student",
        back_populates="quiz_attempts"
    )

    quiz = relationship(
        "Quiz",
        back_populates="attempts"
    )

    # ======================================================
    # Representation
    # ======================================================

    def __repr__(self):

        return (
            f"<QuizAttempt("
            f"id={self.id}, "
            f"student_id={self.student_id}, "
            f"quiz_id={self.quiz_id}, "
            f"score={self.score}, "
            f"passed={self.passed}"
            f")>"
        )