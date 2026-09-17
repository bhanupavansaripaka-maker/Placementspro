"""
==========================================================
PlacementsPro
Application Configuration
==========================================================
"""

APP_NAME = "PlacementsPro"

APP_DESCRIPTION = "Learn Today. Lead Tomorrow."

VERSION = "0.3.0"

HOST = "127.0.0.1"

PORT = 8000


# ==========================================================
# JWT Configuration
# ==========================================================

SECRET_KEY = "skillforge-super-secret-key-change-in-production"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60