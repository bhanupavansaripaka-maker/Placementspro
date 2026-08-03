"""
==========================================================
SkillForge AI
Curriculum Prompt
==========================================================
"""


CURRICULUM_PROMPT = """
You are an expert Technical Curriculum Designer.

Generate a professional course curriculum.

Course Name:
{course_name}

Difficulty:
{difficulty}

Duration:
{duration}

Target Audience:
{target_audience}

Requirements:

1. Generate 8 to 12 modules.

2. Each module should contain 5 to 8 lessons.

3. Arrange modules from beginner to advanced.

4. Include practical topics.

5. Include one capstone project module.

IMPORTANT:

Return ONLY valid JSON.

Format:

{{
    "course": "{course_name}",
    "modules": [
        {{
            "title": "",
            "description": "",
            "lessons": [
                {{
                    "title": ""
                }}
            ]
        }}
    ]
}}

Do not return markdown.

Do not return explanations.

Only JSON.
"""