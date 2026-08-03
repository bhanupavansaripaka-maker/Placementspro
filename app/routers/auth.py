"""
==========================================================
SkillForge Platform
Authentication Router
==========================================================
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.auth import (
    UserRegister,
    UserLogin
)

from app.services.auth_service import AuthService

from app.core.security import get_current_user

from app.models.user import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ==========================================================
# Register
# ==========================================================

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    """

    try:

        new_user = AuthService.register(
            db,
            user
        )

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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong."
        )


# ==========================================================
# Login
# ==========================================================

@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Authenticate user.
    """

    try:

        return AuthService.login(
            db,
            user.email,
            user.password
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

    except Exception as e:

        print("\n================ LOGIN ERROR ================\n")
        import traceback
        traceback.print_exc()
        print("\n=============================================\n")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
# ==========================================================
# Current User
# ==========================================================

@router.get("/me")
def me(
    current_user: User = Depends(get_current_user)
):
    """
    Get currently logged-in user.
    """

    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active
    }