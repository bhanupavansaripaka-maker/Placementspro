"""
==========================================================
SkillForge LMS
Lesson Database Model
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


class Lesson(Base):
    """
    Lesson Database Model
    """

    __tablename__ = "lessons"

    # ==================================================
    # Columns
    # ==================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    module_id: Mapped[int] = mapped_column(
        ForeignKey("modules.id"),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    topic: Mapped[str] = mapped_column(
        String(300),
        nullable=False
    )

    keywords: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    difficulty: Mapped[str] = mapped_column(
        String(30),
        default="Beginner",
        nullable=False
    )

    estimated_minutes: Mapped[int] = mapped_column(
        Integer,
        default=15,
        nullable=False
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

    # ==================================================
    # Relationships
    # ==================================================

    module = relationship(
        "Module",
        back_populates="lessons"
    )

    # ==================================================
    # AI Lesson Content
    # ==================================================

    content = relationship(
        "LessonContent",
        back_populates="lesson",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # ==================================================
    # AI Quiz
    # ==================================================

    quiz = relationship(
        "Quiz",
        back_populates="lesson",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # ==================================================
    # Representation
    # ==================================================

    def __repr__(self):

        return (
            f"<Lesson("
            f"id={self.id}, "
            f"title='{self.title}'"
            f")>"
        )