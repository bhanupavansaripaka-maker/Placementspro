from app.core.security import (
    hash_password,
    verify_password
)

password = "SkillForge@123"

hashed = hash_password(password)

print("Original :", password)
print("Hash     :", hashed)

print(
    verify_password(
        password,
        hashed
    )
)