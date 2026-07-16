"""
==========================================================
SkillForge Platform
Authentication Router
==========================================================
"""
from app.schemas.auth import (
    UserRegister,
    UserLogin
)

from app.services.auth_service import (
    register_user,
    login_user
)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import UserRegister
from app.services.auth_service import register_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", status_code=201)
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    """

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
    """
    Login user.
    """

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