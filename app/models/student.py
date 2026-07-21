"""
==========================================================
SkillForge Platform
Student Model
==========================================================
"""

from sqlalchemy import (
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.core.database import Base


class Student(Base):
    """
    Student Profile Model
    """

    __tablename__ = "students"

    # ==================================================
    # Columns
    # ==================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    college: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    education: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    branch: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    graduation_year: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    profile_photo: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    resume: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    # ==================================================
    # Relationships
    # ==================================================

    user = relationship(
        "User",
        back_populates="student"
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Student(id={self.id}, "
            f"user_id={self.user_id})>"
        )