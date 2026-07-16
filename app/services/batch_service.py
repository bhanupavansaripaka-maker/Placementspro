"""
==========================================================
SkillForge Academy
Batch Service
==========================================================
"""

from app.data.batches import UPCOMING_BATCHES


def get_upcoming_batches():
    """
    Returns all upcoming batches.
    """

    return UPCOMING_BATCHES