"""
==========================================================
SkillForge Academy
Home Service
==========================================================
"""

from app.data.home import (
    HOME_STATISTICS,
    WHY_CHOOSE,
    CALL_TO_ACTION
)

from app.data.courses import FEATURED_COURSES

from app.services.learning_journey_service import get_learning_journey
from app.services.testimonial_service import get_success_stories
from app.services.batch_service import get_upcoming_batches
from app.services.trainer_service import get_corporate_trainings


def get_home_page_data():
    """
    Returns all data required for the homepage.
    """

    return {

        "statistics": HOME_STATISTICS,

        "courses": FEATURED_COURSES,

        "why_choose": WHY_CHOOSE,

        "learning_journey": get_learning_journey(),

        "success_stories": get_success_stories(),

        "upcoming_batches": get_upcoming_batches(),

        "corporate_trainings": get_corporate_trainings(),

        "cta": CALL_TO_ACTION

    }