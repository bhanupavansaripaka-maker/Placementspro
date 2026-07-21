"""
==========================================================
SkillForge Platform
Authentication Schemas
==========================================================
"""

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """
    User Registration Request
    """

    full_name: str = Field(
        min_length=3,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=100
    )


class UserLogin(BaseModel):
    """
    User Login Request
    """

    email: EmailStr
    password: str


class Token(BaseModel):
    """
    JWT Token Response
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    JWT Payload
    """

    email: str | None = None