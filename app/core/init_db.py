"""
==========================================================
SkillForge Platform
Database Initialization
==========================================================
"""

from app.core.database import engine
from app.database.base import Base


def init_db():
    """
    Create all database tables.
    """
    Base.metadata.create_all(bind=engine)