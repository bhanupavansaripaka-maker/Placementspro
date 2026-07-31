"""
==========================================================
SkillForge Platform
Student Schemas
==========================================================
"""

from pydantic import BaseModel, Field, ConfigDict


# ==========================================================
# Profile Create / Update
# ==========================================================

class StudentProfileCreate(BaseModel):

    phone: str | None = Field(default=None, max_length=20)

    college: str | None = Field(default=None, max_length=150)

    education: str | None = Field(default=None, max_length=100)

    branch: str | None = Field(default=None, max_length=100)

    graduation_year: int | None = None

    profile_photo: str | None = None

    resume: str | None = None


# ==========================================================
# Profile Update
# ==========================================================

class StudentProfileUpdate(BaseModel):

    phone: str | None = Field(default=None, max_length=20)

    college: str | None = Field(default=None, max_length=150)

    education: str | None = Field(default=None, max_length=100)

    branch: str | None = Field(default=None, max_length=100)

    graduation_year: int | None = None

    profile_photo: str | None = None

    resume: str | None = None


# ==========================================================
# Profile Response
# ==========================================================

class StudentProfileResponse(BaseModel):

    id: int

    full_name: str

    email: str

    phone: str | None

    college: str | None

    education: str | None

    branch: str | None

    graduation_year: int | None

    profile_photo: str | None

    resume: str | None

    model_config = ConfigDict(
        from_attributes=True
    )