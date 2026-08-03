"""
==========================================================
SkillForge AI
AI Manager
==========================================================
"""

from app.ai.config import AIConfig

from app.ai.providers.openai_provider import OpenAIProvider


class AIManager:
    """
    Returns the configured AI Provider.
    """

    @staticmethod
    def get_provider():

        provider = AIConfig.PROVIDER.lower()

        if provider == "openai":

            return OpenAIProvider()

        raise ValueError(
            f"Unsupported AI Provider: {provider}"
        )