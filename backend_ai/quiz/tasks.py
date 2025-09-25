from celery import shared_task
from .services import generate_quiz
import json
import time


@shared_task
def generate_quiz_task(question_count, difficulty, question_type, content, user_id):
    try:
        quiz = generate_quiz(question_count, difficulty, question_type, content)
        return {"user_id": user_id, "data": quiz.dict()}
    except Exception as e:
        raise Exception(f"Quiz generation failed: {str(e)}")
