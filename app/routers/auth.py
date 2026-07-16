"""
==========================================================
SkillForge Platform
Authentication Router
==========================================================
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import (
    UserRegister,
    UserLogin
)

from app.services.auth_service import (
    register_user,
    login_user
)

from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", status_code=201)
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    try:

        new_user = register_user(db, user)

        return {
            "success": True,
            "message": "User registered successfully.",
            "user": {
                "id": new_user.id,
                "full_name": new_user.full_name,
                "email": new_user.email,
                "role": new_user.role
            }
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    try:

        return login_user(
            db,
            user.email,
            user.password
        )

    except ValueError as e:

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )


@router.get("/me")
def me(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active
    }