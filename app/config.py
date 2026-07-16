"""
Application Configuration
"""
APP_NAME = "SkillForge LMS"
APP_DESCRIPTION = "Learning Management System"
VERSION = "1.0.0"
HOST = "127.0.0.1"
PORT = 8000

"""
==========================================================
Application Configuration
==========================================================
"""

APP_NAME = "SkillForge Platform"

APP_DESCRIPTION = "Learn Today. Lead Tomorrow."

VERSION = "0.3.0"

# ==========================================================
# JWT Configuration
# ==========================================================

SECRET_KEY = "skillforge-super-secret-key-change-in-production"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60