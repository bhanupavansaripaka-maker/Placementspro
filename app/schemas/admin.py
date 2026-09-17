"""
==========================================================
SkillForge LMS
Admin Schemas
==========================================================
"""

from pydantic import BaseModel


# ==========================================================
# Dashboard Statistics
# ==========================================================

class AdminDashboardStatistics(BaseModel):

    students: int

    courses: int

    enrollments: int

    ai_generated: int


# ==========================================================
# Update Course Request
# ==========================================================

class UpdateCourseRequest(BaseModel):

    title: str

    description: str

    category: str

    level: str

    duration: int

    price: int


# ==========================================================
# Create Module Request
# ==========================================================

class CreateModuleRequest(BaseModel):

    title: str

    description: str | None = None
# ==========================================================
# Update Module Request
# ==========================================================

class UpdateModuleRequest(BaseModel):

    title: str

    description: str | None = None