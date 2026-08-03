"""
==========================================================
SkillForge Platform
Module Schemas
==========================================================
"""

from pydantic import BaseModel, ConfigDict


# ==========================================================
# Create Module
# ==========================================================

class ModuleCreate(BaseModel):

    course_id: int

    title: str

    description: str | None = None

    display_order: int = 1


# ==========================================================
# Update Module
# ==========================================================

class ModuleUpdate(BaseModel):

    title: str | None = None

    description: str | None = None

    display_order: int | None = None

    is_active: bool | None = None


# ==========================================================
# Module Response
# ==========================================================

class ModuleResponse(BaseModel):

    id: int

    course_id: int

    title: str

    description: str | None

    display_order: int

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )