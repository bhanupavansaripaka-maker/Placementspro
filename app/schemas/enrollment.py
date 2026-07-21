"""
==========================================================
SkillForge Platform
Enrollment Schemas
==========================================================
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ==========================================================
# Create Enrollment
# ==========================================================

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


# ==========================================================
# Enrollment Response
# ==========================================================

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# Student Courses Response
# ==========================================================

class StudentCourseResponse(BaseModel):
    course_id: int
    title: str
    category: str
    level: str
    duration: int
    price: int
    enrolled_at: datetime