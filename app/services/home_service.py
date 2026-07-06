"""
Home Service

Responsible for preparing all data required by the homepage.
"""

from app.data.courses import courses


class HomeService:

    @staticmethod
    def get_homepage_data():

        return {

            "hero": {

                "tag": "🚀 India's Emerging EdTech Platform",

                "title": "Learn Today.",

                "highlight": "Lead Tomorrow.",

                "description": (
                    "Master Python, Java, Full Stack Development, "
                    "Data Science, Artificial Intelligence and "
                    "Campus Recruitment Training with Industry Experts."
                )

            },

            "stats": {

                "students": "1000+",

                "courses": "50+",

                "placements": "95%",

                "corporates": "10+"

            },

            "featured_courses": courses[:4]

        }