"""
==========================================================
SkillForge Platform
Course Schemas
==========================================================
"""

from pydantic import BaseModel, Field


class CourseCreate(BaseModel):
    title: str = Field(..., max_length=150)
    description: str
    category: str = Field(..., max_length=100)
    level: str = Field(..., max_length=50)
    duration: int
    price: int = 0


class CourseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    level: str | None = None
    duration: int | None = None
    price: int | None = None
    is_active: bool | None = None


class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    level: str
    duration: int
    price: int
    is_active: bool

    model_config = {
        "from_attributes": True
    }