"""
==========================================================
SkillForge LMS
OpenAI AI Provider
==========================================================
"""

import json

from openai import OpenAI

from app.ai.config import AIConfig
from app.ai.providers.base import BaseAIProvider

from app.ai.prompts.curriculum import CURRICULUM_PROMPT
from app.ai.prompts.lesson import LESSON_CONTENT_PROMPT
from app.ai.prompts.quiz import QUIZ_PROMPT


class OpenAIProvider(BaseAIProvider):
    """
    OpenAI AI Provider
    """

    # ======================================================
    # Initialization
    # ======================================================

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

            print()
            print("=" * 70)
            print("AI CURRICULUM RAW RESPONSE")
            print("=" * 70)
            print(content)
            print("=" * 70)
            print()

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
        course_name: str,
        module_title: str,
        lesson_title: str,
        topic: str,
        difficulty: str,
        target_audience: str = "Engineering Students"
    ):

        prompt = LESSON_CONTENT_PROMPT.format(
            course_name=course_name,
            module_title=module_title,
            lesson_title=lesson_title,
            topic=topic,
            difficulty=difficulty,
            target_audience=target_audience
        )

        try:

            response = self.client.responses.create(
                model=AIConfig.OPENAI_MODEL,
                input=prompt,
                max_output_tokens=AIConfig.MAX_TOKENS
            )

            content = response.output_text

            print()
            print("=" * 70)
            print("AI LESSON RAW RESPONSE")
            print("=" * 70)
            print(content)
            print("=" * 70)
            print()

            return json.loads(content)

        except json.JSONDecodeError:

            raise ValueError(
                "AI returned invalid JSON for lesson."
            )

        except Exception as e:

            raise RuntimeError(
                f"OpenAI Lesson Error: {str(e)}"
            )

    # ======================================================
    # Generate Quiz
    # ======================================================

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

        prompt = QUIZ_PROMPT.format(
            course_name=course_name,
            module_title=module_title,
            lesson_title=lesson_title,
            topic=topic,
            difficulty=difficulty,
            number_of_questions=number_of_questions,
            target_audience=target_audience
        )

        try:

            response = self.client.responses.create(
                model=AIConfig.OPENAI_MODEL,
                input=prompt,
                max_output_tokens=AIConfig.MAX_TOKENS
            )

            content = response.output_text

            print()
            print("=" * 70)
            print("AI QUIZ RAW RESPONSE")
            print("=" * 70)
            print(content)
            print("=" * 70)
            print()

            quiz = json.loads(content)

            # ==================================================
            # Validate Quiz Structure
            # ==================================================

            if not isinstance(quiz, dict):

                raise ValueError(
                    "AI returned invalid quiz structure."
                )

            required_quiz_fields = [

                "title",
                "description",
                "difficulty",
                "passing_score",
                "questions"

            ]

            for field in required_quiz_fields:

                if field not in quiz:

                    raise ValueError(
                        f"AI quiz response is missing "
                        f"field: {field}"
                    )

            if not isinstance(
                quiz["questions"],
                list
            ):

                raise ValueError(
                    "AI questions must be a list."
                )

            # ==================================================
            # Validate Question Count
            # ==================================================

            if len(
                quiz["questions"]
            ) != number_of_questions:

                raise ValueError(
                    f"AI returned "
                    f"{len(quiz['questions'])} questions "
                    f"instead of "
                    f"{number_of_questions}."
                )

            # ==================================================
            # Validate Questions
            # ==================================================

            required_question_fields = [

                "question",
                "option_a",
                "option_b",
                "option_c",
                "option_d",
                "correct_answer",
                "explanation"

            ]

            for index, question in enumerate(
                quiz["questions"],
                start=1
            ):

                if not isinstance(
                    question,
                    dict
                ):

                    raise ValueError(
                        f"Question {index} "
                        f"has invalid format."
                    )

                for field in required_question_fields:

                    if field not in question:

                        raise ValueError(
                            f"Question {index} "
                            f"is missing field: {field}"
                        )

                    if (
                        question[field] is None
                        or str(
                            question[field]
                        ).strip() == ""
                    ):

                        raise ValueError(
                            f"Question {index} "
                            f"has empty field: {field}"
                        )

                # ==============================================
                # Validate Correct Answer
                # ==============================================

                correct_answer = str(
                    question["correct_answer"]
                ).upper().strip()

                if correct_answer not in {
                    "A",
                    "B",
                    "C",
                    "D"
                }:

                    raise ValueError(
                        f"Question {index} "
                        f"has invalid correct_answer: "
                        f"{correct_answer}"
                    )

                question["correct_answer"] = (
                    correct_answer
                )

            # ==================================================
            # Validate Passing Score
            # ==================================================

            try:

                passing_score = int(
                    quiz["passing_score"]
                )

            except (
                TypeError,
                ValueError
            ):

                raise ValueError(
                    "AI returned invalid passing_score."
                )

            if not 0 <= passing_score <= 100:

                raise ValueError(
                    "Passing score must be between 0 and 100."
                )

            quiz["passing_score"] = passing_score

            return quiz

        except json.JSONDecodeError:

            raise ValueError(
                "AI returned invalid JSON for quiz."
            )

        except ValueError:

            raise

        except Exception as e:

            raise RuntimeError(
                f"OpenAI Quiz Error: {str(e)}"
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