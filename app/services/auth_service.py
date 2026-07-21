"""
==========================================================
SkillForge Platform
Authentication Service
==========================================================
"""

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.student import Student

from app.schemas.auth import UserRegister

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


def register_user(db: Session, user: UserRegister):
    """
    Register a new user and create the linked student profile.
    """

    # Check if email already exists
    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise ValueError("Email already registered.")

    try:
        # -----------------------------
        # Create User
        # -----------------------------
        new_user = User(
            full_name=user.full_name,
            email=user.email,
            password_hash=hash_password(user.password),
            role="student"
        )

        db.add(new_user)
        db.flush()      # Generates new_user.id without committing

        # -----------------------------
        # Create Student Profile
        # -----------------------------
        student = Student(
            user_id=new_user.id
        )

        db.add(student)

        db.commit()

        db.refresh(new_user)
        db.refresh(student)

        return new_user

    except Exception:
        db.rollback()
        raise


def login_user(db: Session, email: str, password: str):
    """
    Authenticate user.
    """

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        raise ValueError("Invalid email or password.")

    if not verify_password(
        password,
        user.password_hash
    ):
        raise ValueError("Invalid email or password.")

    access_token = create_access_token(
        {
            "sub": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


def get_user_by_email(db: Session, email: str):
    """
    Get user by email.
    """

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )