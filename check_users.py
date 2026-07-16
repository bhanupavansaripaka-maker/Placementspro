from app.core.database import SessionLocal
from app.models.user import User

db = SessionLocal()

users = db.query(User).all()

print("=" * 60)
print("Registered Users")
print("=" * 60)

for user in users:
    print(f"ID    : {user.id}")
    print(f"Name  : {user.full_name}")
    print(f"Email : {user.email}")
    print("-" * 60)

db.close()