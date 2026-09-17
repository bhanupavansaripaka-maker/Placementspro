"""
==========================================================
SkillForge LMS
Lesson Content Database Model
==========================================================
"""

from sqlalchemy import (
    Integer,
    Text,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.core.database import Base


class LessonContent(Base):
    """
    AI generated content for a lesson.
    """

    __tablename__ = "lesson_contents"


    # ==================================================
    # Columns
    # ==================================================

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


    explanation: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )


    learning_objectives: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )


    examples: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )


    code_examples: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )


    practical_exercise: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )


    key_points: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )


    # ==================================================
    # Relationship
    # ==================================================

    lesson = relationship(
        "Lesson",
        back_populates="content"
    )


    # ==================================================
    # Representation
    # ==================================================

    def __repr__(self):

        return (
            f"<LessonContent("
            f"id={self.id}, "
            f"lesson_id={self.lesson_id}"
            f")>"
        )