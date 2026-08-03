"""
==========================================================
SkillForge AI
Base Provider
==========================================================
"""

from abc import ABC, abstractmethod


class BaseAIProvider(ABC):
    """
    Base class for every AI provider.
    """

    @abstractmethod
    def generate_curriculum(
        self,
        course_name: str,
        difficulty: str,
        duration: str,
        target_audience: str
    ):
        """
        Generate curriculum.
        """
        pass

    @abstractmethod
    def generate_lesson(
        self,
        lesson_title: str,
        difficulty: str
    ):
        """
        Generate lesson content.
        """
        pass

    @abstractmethod
    def generate_quiz(
        self,
        lesson_title: str
    ):
        """
        Generate quiz.
        """
        pass

    @abstractmethod
    def generate_coding_questions(
        self,
        lesson_title: str
    ):
        """
        Generate coding questions.
        """
        pass

    @abstractmethod
    def chat(
        self,
        question: str,
        context: str
    ):
        """
        AI tutor chat.
        """
        pass