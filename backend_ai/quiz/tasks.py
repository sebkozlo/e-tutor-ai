from celery import shared_task
from quiz.services.quiz_generator import generate_quiz
from .models import Quiz
from core.models import ExternalUser


@shared_task
def generate_quiz_task(
    question_count, difficulty, question_type, content, external_uuid
):
    try:
        result = generate_quiz(question_count, difficulty, question_type, content)

        external_user = ExternalUser.objects.get(external_id=external_uuid)

        quiz = Quiz.objects.create_with_token_usage(
            external_user=external_user,
            question_count=question_count,
            difficulty=difficulty,
            question_type=question_type,
            content=content,
            usage_data=result["usage"],
        )

        return {
            "quiz": result["quiz_data"],
            "external_user_id": str(external_user.external_id),
        }

    except Exception as e:
        raise Exception(f"Quiz generation failed: {str(e)}")

    except ExternalUser.DoesNotExist:
        raise Exception(f"User {external_uuid} not found")
