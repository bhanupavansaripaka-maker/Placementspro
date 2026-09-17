"""
==========================================================
SkillForge LMS
Quiz Models
==========================================================
"""

from sqlalchemy import (
    Integer,
    String,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.core.database import Base


# ==========================================================
# Quiz
# ==========================================================

class Quiz(Base):
    """
    Quiz associated with a lesson.
    """

    __tablename__ = "quizzes"

    # ======================================================
    # Columns
    # ======================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id"),
        nullable=False,
        unique=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(1000),
        nullable=True
    )

    difficulty: Mapped[str] = mapped_column(
        String(30),
        default="Beginner",
        nullable=False
    )

    passing_score: Mapped[int] = mapped_column(
        Integer,
        default=60,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    # ======================================================
    # Relationships
    # ======================================================

    lesson = relationship(
        "Lesson",
        back_populates="quiz"
    )

    questions = relationship(
        "QuizQuestion",
        back_populates="quiz",
        cascade="all, delete-orphan",
        order_by="QuizQuestion.display_order"
    )

    # ------------------------------------------------------
    # Quiz Attempts
    # ------------------------------------------------------

    attempts = relationship(
        "QuizAttempt",
        back_populates="quiz",
        cascade="all, delete-orphan"
    )

    # ======================================================
    # Representation
    # ======================================================

    def __repr__(self):

        return (
            f"<Quiz("
            f"id={self.id}, "
            f"title='{self.title}'"
            f")>"
        )


# ==========================================================
# Quiz Question
# ==========================================================

class QuizQuestion(Base):
    """
    Individual question belonging to a quiz.
    """

    __tablename__ = "quiz_questions"

    # ======================================================
    # Columns
    # ======================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    quiz_id: Mapped[int] = mapped_column(
        ForeignKey("quizzes.id"),
        nullable=False
    )

    question: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    option_a: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    option_b: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    option_c: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    option_d: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    correct_answer: Mapped[str] = mapped_column(
        String(1),
        nullable=False
    )

    explanation: Mapped[str] = mapped_column(
        String(2000),
        nullable=True
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    # ======================================================
    # Relationships
    # ======================================================

    quiz = relationship(
        "Quiz",
        back_populates="questions"
    )

    # ======================================================
    # Representation
    # ======================================================

    def __repr__(self):

        return (
            f"<QuizQuestion("
            f"id={self.id}, "
            f"quiz_id={self.quiz_id}"
            f")>"
        )