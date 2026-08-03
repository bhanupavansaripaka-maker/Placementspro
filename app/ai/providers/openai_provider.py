"""
==========================================================
SkillForge AI
OpenAI Provider
==========================================================
"""

import json

from openai import OpenAI

from app.ai.config import AIConfig
from app.ai.providers.base import BaseAIProvider
from app.ai.prompts.curriculum import CURRICULUM_PROMPT


class OpenAIProvider(BaseAIProvider):
    """
    OpenAI AI Provider
    """

    def __init__(self):

        self.client = OpenAI(
            api_key=AIConfig.OPENAI_API_KEY
        )

    # ======================================================
    # Generate Curriculum
    # ======================================================

    def generate_curriculum(
        self,
        course_name: str,
        difficulty: str,
        duration: str,
        target_audience: str
    ):

        prompt = CURRICULUM_PROMPT.format(
            course_name=course_name,
            difficulty=difficulty,
            duration=duration,
            target_audience=target_audience
        )

        try:

            response = self.client.responses.create(
                model=AIConfig.OPENAI_MODEL,
                input=prompt,
                max_output_tokens=AIConfig.MAX_TOKENS
            )

            content = response.output_text

            return json.loads(content)

        except json.JSONDecodeError:

            raise ValueError(
                "AI returned invalid JSON."
            )

        except Exception as e:

            raise RuntimeError(
                f"OpenAI Error: {str(e)}"
            )

    # ======================================================
    # Generate Lesson
    # ======================================================

    def generate_lesson(
        self,
        lesson_title: str,
        difficulty: str
    ):

        raise NotImplementedError(
            "Lesson generation is not implemented yet."
        )

    # ======================================================
    # Generate Quiz
    # ======================================================

    def generate_quiz(
        self,
        lesson_title: str
    ):

        raise NotImplementedError(
            "Quiz generation is not implemented yet."
        )

    # ======================================================
    # Generate Coding Questions
    # ======================================================

    def generate_coding_questions(
        self,
        lesson_title: str
    ):

        raise NotImplementedError(
            "Coding question generation is not implemented yet."
        )

    # ======================================================
    # AI Tutor Chat
    # ======================================================

    def chat(
        self,
        question: str,
        context: str
    ):

        raise NotImplementedError(
            "AI Tutor is not implemented yet."
        )