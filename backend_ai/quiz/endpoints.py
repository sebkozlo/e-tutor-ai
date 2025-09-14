from typing import Dict, List
from ninja import Router
from .schemas import (
    QuizRequestSchema,
    QuizResponseListSchema,
    SolutionResponseSchema,
    SolutionRequestSchema,
    SolutionRequestListSchema,
    SolutionRequest,
    QuizRequestListSchema,
    ChoiceSchema,
)
from .openai import generate_quiz, generate_solution
from .models import QuizRequest, QuestionType, DifficultyLevels, Limits


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


@router.post("/solution", response=SolutionResponseSchema, tags=["Quiz"], by_alias=True)
def question_solution_endpoint(request, payload: SolutionRequestSchema) -> Dict:
    solution = generate_solution(payload.question, payload.solution_level)
    SolutionRequest.objects.create(**payload.dict())
    return solution


@router.get(
    "/quiz-requests", response=QuizRequestListSchema, tags=["Quiz"], by_alias=True
)
def get_all_quiz_request(request) -> Dict:
    qs = QuizRequest.objects.all()
    return {"items": list(qs)}


@router.get(
    "/solution-requests",
    response=SolutionRequestListSchema,
    tags=["Quiz"],
    by_alias=True,
)
def get_all_solution_request(request) -> Dict:
    qs = SolutionRequest.objects.all()
    return {"items": list(qs)}


@router.get("/config", response=Dict[str, List], tags=["Quiz"], by_alias=True)
def get_quiz_config(request) -> Dict:
    question_types = [{"id": qt.value, "name": qt.label} for qt in QuestionType]
    difficulty_levels = [{"id": dl.value, "name": dl.label} for dl in DifficultyLevels]
    limits = [{"id": limit.value, "name": str(limit.value)} for limit in Limits]

    return {
        "questionTypes": question_types,
        "difficultyLevels": difficulty_levels,
        "limits": limits,
    }
