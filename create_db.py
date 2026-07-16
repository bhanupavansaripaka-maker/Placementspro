"""
Create Database
"""

from app.core.database import Base, engine

# Import all models

from app.database import base


def create_database():

    Base.metadata.create_all(bind=engine)

    print("=" * 50)
    print("SkillForge Database Created Successfully")
    print("=" * 50)


if __name__ == "__main__":

    create_database()