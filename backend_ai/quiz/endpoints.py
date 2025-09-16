from typing import Dict, List
from ninja import Router, File
from ninja.files import UploadedFile
from .schemas import (
    QuizRequestSchema,
    QuizResponseListSchema,
    SolutionResponseSchema,
    SolutionRequestSchema,
    SolutionRequestListSchema,
    SolutionRequest,
    QuizRequestListSchema,
    UploadSuccess,
    ErrorResponse,
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
    "/quiz-requests", response={200: QuizRequestListSchema}, tags=["Quiz"], by_alias=True
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


@router.post(
    "/upload",
    tags=["Quiz"],
    response={200: UploadSuccess, 400: ErrorResponse, 413: ErrorResponse, 415: ErrorResponse}
)
def upload_file(request, file: File[UploadedFile] = None):
    if not file:
        return 400, {"detail": "No file uploaded."}
    if file.content_type != "text/plain":
        return 415, {"detail": "Invalid file type. Only text files are allowed."}
    if file.size > 5 * 1024 * 1024:
        return 413, {"detail": "File size exceeds the limit of 5MB."}

    return {
        "filename": file.name,
        "size": file.size,
        "message": "File uploaded successfully"
    }