"""
==========================================================
SkillForge Platform
Enrollment Model
==========================================================
"""

from datetime import datetime

from sqlalchemy import (
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


class Enrollment(Base):
    """
    Enrollment Model
    """

    __tablename__ = "enrollments"

    # -----------------------------
    # Columns
    # -----------------------------

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id"),
        nullable=False
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id"),
        nullable=False
    )

    enrolled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # -----------------------------
    # Relationships
    # -----------------------------

    student = relationship(
        "Student",
        back_populates="enrollments"
    )

    course = relationship(
        "Course",
        back_populates="enrollments"
    )

    def __repr__(self):
        return (
            f"<Enrollment(id={self.id}, "
            f"student_id={self.student_id}, "
            f"course_id={self.course_id})>"
        )