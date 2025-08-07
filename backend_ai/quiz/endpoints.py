from django.views.decorators.http import require_http_methods
from typing import Dict
from ninja import Router
from .schemas import (
    QuizRequestSchema,
    SolutionResponseSchema,
    QuizResponseListSchema,
    SolutionRequestSchema,
    SolutionRequest,
    QuizRequestListSchema,
)
from .openai import generate_quiz, generate_solution
from .models import QuizRequest


router = Router()



@router.post("/generate", response=QuizResponseListSchema, tags=["Quiz"], by_alias=True)
def generate_quiz_endpoint(request, payload: QuizRequestSchema) -> Dict:
    quiz = generate_quiz(
        payload.question_count,
        payload.difficulty,
        payload.question_type,
        payload.content,
    )
    QuizRequest.objects.create(**payload.dict())
    return quiz


@router.post("/solution", response=SolutionResponseSchema, tags=["Quiz"])
def question_solution_endpoint(request, payload: SolutionRequestSchema) -> Dict:
    solution = generate_solution(payload.question, payload.solution_level)
    SolutionRequest.objects.create(**payload.dict())
    return solution


@router.get("/quiz-requests", response=QuizRequestListSchema)
def get_all_quiz_request(request) -> Dict:
    qs = QuizRequest.objects.all()
    return {"items": list(qs)}


@router.get("/solution-requests", response=SolutionRequestSchema, by_alias=True)
def get_all_solution_request(request) -> Dict:
    return SolutionRequest.objects.all()
