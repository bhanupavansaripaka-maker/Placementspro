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


    # ======================================================
    # Generate Curriculum
    # ======================================================

    @abstractmethod
    def generate_curriculum(
        self,
        course_name: str,
        difficulty: str,
        duration: str,
        target_audience: str
    ):
        """
        Generate course curriculum.
        """

        pass


    # ======================================================
    # Generate Lesson Content
    # ======================================================

    @abstractmethod
    def generate_lesson(
        self,
        course_name: str,
        module_title: str,
        lesson_title: str,
        topic: str,
        difficulty: str,
        target_audience: str = "Engineering Students"
    ):
        """
        Generate AI lesson content.
        """

        pass


    # ======================================================
    # Generate Quiz
    # ======================================================

    @abstractmethod
    def generate_quiz(
        self,
        course_name: str,
        module_title: str,
        lesson_title: str,
        topic: str,
        difficulty: str,
        number_of_questions: int = 10,
        target_audience: str = "Engineering Students"
    ):
        """
        Generate AI quiz.
        """

        pass


    # ======================================================
    # Generate Coding Questions
    # ======================================================

    @abstractmethod
    def generate_coding_questions(
        self,
        lesson_title: str
    ):
        """
        Generate coding questions.
        """

        pass


    # ======================================================
    # AI Tutor Chat
    # ======================================================

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