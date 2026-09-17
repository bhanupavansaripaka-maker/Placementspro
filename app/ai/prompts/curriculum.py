CURRICULUM_PROMPT = """
You are an expert Technical Curriculum Designer for SkillForge Academy.

Your task is to generate a professional, structured, industry-oriented
technical course curriculum.

Course Name:
{course_name}

Difficulty:
{difficulty}

Duration:
{duration}

Target Audience:
{target_audience}


COURSE DESIGN REQUIREMENTS:

1. Generate 8 to 12 modules.

2. Each module must contain 5 to 8 lessons.

3. Arrange the curriculum logically from foundational concepts
   to intermediate and advanced concepts.

4. The curriculum should be suitable for the specified target audience.

5. Include practical and hands-on topics wherever appropriate.

6. Include programming exercises, practical activities, or implementation
   topics where relevant to the course.

7. Include one dedicated capstone project module near the end of the course.

8. Do not repeat the same topic across multiple lessons.

9. Lesson titles must be specific and meaningful.

10. The estimated lesson duration should be realistic.

11. Lesson difficulty should reflect the complexity of the lesson.

12. Keywords should contain important technical concepts covered by
    the lesson.


MODULE REQUIREMENTS:

Each module must contain:

- title
- description
- lessons


LESSON REQUIREMENTS:

Each lesson must contain:

- title
- topic
- keywords
- difficulty
- estimated_minutes


LESSON FIELD RULES:

title:
A concise and meaningful lesson title.

topic:
A short description of what the lesson teaches.

keywords:
An array of important technical concepts covered by the lesson.

difficulty:
Use one of:
"Beginner"
"Intermediate"
"Advanced"

estimated_minutes:
An integer representing the estimated time required to complete
the lesson.


CAPSTONE MODULE:

The final module should contain a practical capstone project.

The capstone should include lessons covering:

- Project requirements
- Architecture or design
- Implementation
- Testing
- Deployment or presentation


IMPORTANT OUTPUT RULES:

Return ONLY valid JSON.

Do not return Markdown.

Do not return explanations.

Do not wrap the JSON inside ```json or ```.

Use exactly this structure:

{{
    "course": "{course_name}",
    "modules": [
        {{
            "title": "",
            "description": "",
            "lessons": [
                {{
                    "title": "",
                    "topic": "",
                    "keywords": [],
                    "difficulty": "",
                    "estimated_minutes": 30
                }}
            ]
        }}
    ]
}}

The JSON must be syntactically valid.

Do not add fields outside the specified structure.
"""