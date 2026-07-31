"""
==========================================================
SkillForge Platform
Dashboard Schemas
==========================================================
"""

from pydantic import BaseModel, ConfigDict


class DashboardStatistics(BaseModel):
    """
    Dashboard statistics response schema.
    """

    enrolled_courses: int
    available_courses: int
    categories: int
    profile_completed: bool

    model_config = ConfigDict(from_attributes=True)