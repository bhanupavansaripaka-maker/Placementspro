from app.services.ai.curriculum_service import CurriculumService

result = CurriculumService.generate(
    course_name="Python Full Stack Development",
    difficulty="Beginner",
    duration="3 Months",
    target_audience="Freshers"
)

print(result)