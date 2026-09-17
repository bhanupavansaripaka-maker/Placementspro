"""
==========================================================
SkillForge LMS
Lesson Progress Model
==========================================================
"""

from datetime import datetime

from sqlalchemy import (
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy.sql import func

from app.core.database import Base


class LessonProgress(Base):
    """
    Tracks a student's progress for an individual lesson.
    """

    __tablename__ = "lesson_progress"

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
        nullable=False
    )

    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id"),
        nullable=False
    )

    started: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # ======================================================
    # Constraints
    # ======================================================

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "lesson_id",
            name="uq_student_lesson_progress"
        ),
    )

    # ======================================================
    # Relationships
    # ======================================================

    student = relationship(
        "Student",
        back_populates="lesson_progress"
    )

    lesson = relationship(
        "Lesson",
        back_populates="progress_records"
    )

    # ======================================================
    # Representation
    # ======================================================

    def __repr__(self):

        return (
            f"<LessonProgress("
            f"id={self.id}, "
            f"student_id={self.student_id}, "
            f"lesson_id={self.lesson_id}, "
            f"completed={self.completed}"
            f")>"
        )