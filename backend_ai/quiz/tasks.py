from celery import shared_task
from .services import generate_quiz
from core.models import ExternalUser
import json
import time


@shared_task
def generate_quiz_task(question_count, difficulty, question_type, content, user_id):
    try:
        user = ExternalUser.objects.get(id=user_id)
        quiz = generate_quiz(question_count, difficulty, question_type, content)

        return {"external_user_id": str(user.external_id), "data": quiz.dict()}
    except Exception as e:
        raise Exception(f"Quiz generation failed: {str(e)}")