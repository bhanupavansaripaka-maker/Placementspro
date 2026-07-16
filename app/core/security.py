"""
==========================================================
SkillForge Platform
Security Utilities
==========================================================
"""

from datetime import datetime, timedelta, UTC

import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

from app.database import get_db

# ==========================================================
# Password Hashing Configuration
# ==========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ==========================================================
# HTTP Bearer Authentication
# ==========================================================

security = HTTPBearer()


# ==========================================================
# Password Utilities
# ==========================================================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ==========================================================
# JWT Utilities
# ==========================================================

def create_access_token(data: dict) -> str:

    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_access_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except InvalidTokenError:

        return None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Return authenticated user.
    """

    from app.models.user import User

    token = credentials.credentials

    payload = decode_access_token(token)

    if payload is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token."
        )

    email = payload.get("sub")

    if email is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid token."
        )

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    return user