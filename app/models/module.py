"""
==========================================================
SkillForge Platform
Module Model
==========================================================
"""

from sqlalchemy import (
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.core.database import Base


class Module(Base):
    """
    Course Module Model
    """

    __tablename__ = "modules"

    # ==================================================
    # Columns
    # ==================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id"),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
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

    # ==================================================
    # Relationships
    # ==================================================

    course = relationship(
        "Course",
        back_populates="modules"
    )

    lessons = relationship(
        "Lesson",
        back_populates="module",
        cascade="all, delete-orphan",
        order_by="Lesson.display_order"
    )

    # ==================================================
    # String Representation
    # ==================================================

    def __repr__(self):
        return (
            f"<Module(id={self.id}, "
            f"title='{self.title}', "
            f"course_id={self.course_id})>"
        )