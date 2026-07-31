from app.core.database import SessionLocal
from app.models.user import User

db = SessionLocal()

users = db.query(User).all()

for user in users:
    print("----------------------------")
    print("ID:", user.id)
    print("Name:", user.full_name)
    print("Email:", user.email)
    print("Password:", user.password)
    print("Role:", user.role)