"""
==========================================================
SkillForge Platform
Course Model
==========================================================
"""

from sqlalchemy import (
    Boolean,
    Integer,
    String,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.core.database import Base


class Course(Base):
    """
    Course Database Model
    """

    __tablename__ = "courses"

    # ==================================================
    # Columns
    # ==================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    level: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    duration: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    price: Mapped[int] = mapped_column(
        Integer,
        default=0,
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

    enrollments = relationship(
        "Enrollment",
        back_populates="course",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Course(id={self.id}, "
            f"title='{self.title}', "
            f"category='{self.category}')>"
        )