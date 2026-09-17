"""
==========================================================
SkillForge AI
Configuration
==========================================================
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# ----------------------------------------------------------
# Load .env from project root
# ----------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")


class AIConfig:
    """
    Central AI Configuration
    """

    # ======================================================
    # Active Provider
    # ======================================================

    PROVIDER = os.getenv(
        "AI_PROVIDER",
        "openai"
    )

    # ======================================================
    # OpenAI
    # ======================================================

    OPENAI_API_KEY = os.getenv(
        "OPENAI_API_KEY"
    )

    OPENAI_MODEL = os.getenv(
        "OPENAI_MODEL",
        "gpt-5"
    )

    # ======================================================
    # Claude
    # ======================================================

    CLAUDE_API_KEY = os.getenv(
        "CLAUDE_API_KEY"
    )

    CLAUDE_MODEL = os.getenv(
        "CLAUDE_MODEL",
        "claude-sonnet-4"
    )

    # ======================================================
    # Gemini
    # ======================================================

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY"
    )

    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-pro"
    )

    # ======================================================
    # AI Settings
    # ======================================================

    TEMPERATURE = 0.7

    MAX_TOKENS = 12000