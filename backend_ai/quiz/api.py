from typing import Dict, List
from ninja import Router, File
from ninja.errors import HttpError
from ninja.files import UploadedFile
from .schemas import (
    QuizRequestSchema,
    SolutionResponseSchema,
    SolutionRequestSchema,
    SolutionRequestOutSchema,
    QuizRequestOutSchema,
    UploadSuccess,
)

from users.services.user_service import (
    get_external_user_from_request,
    get_existing_external_user,
)
from .tasks import generate_quiz_task
from .models import Quiz, QuizSolution, QuestionType, DifficultyLevels, Limits
from ninja.pagination import PageNumberPagination, paginate


router = Router()


@router.post("/quizzes", by_alias=True)
def generate_quiz_endpoint(request, payload: QuizRequestSchema):
    external_user = get_external_user_from_request(request)

    task = generate_quiz_task.delay(
        payload.question_count,
        payload.difficulty,
        payload.question_type,
        payload.content,
        str(external_user.external_id),
    )

    return {
        "task_id": task.id,
        "status": "PENDING",
        "_link": f"/quizzes/result/{task.id}",
        "message": "Quiz generation started",
    }


@router.get("/quizzes/result/{task_id}", by_alias=True)
def get_quiz_result(request, task_id: str):
    external_user = get_existing_external_user(request)

    result = generate_quiz_task.AsyncResult(task_id)

    if result.state == "PENDING":
        return {"status": "PENDING", "message": "Quiz generation is still in progress."}
    elif result.state == "FAILURE":
        return {"status": "FAILURE", "message": str(result.info)}
    elif result.state == "SUCCESS":
        task_result = result.result
        if str(external_user.external_id) != task_result.get("external_user_id"):
            raise HttpError(403, "Forbidden: You do not have access to this task.")
        return {
            "status": "SUCCESS",
            "data": task_result.get("quiz"),
            "message": "Quiz generation completed successfully.",
        }
    else:
        return {"status": result.state, "message": "Quiz generation is in progress."}


@router.get("/quizzes", response=List[QuizRequestOutSchema], by_alias=True)
@paginate(PageNumberPagination, page_size=10, max_page_size=50)
def get_all_quiz_request(request):
    external_user = get_existing_external_user(request)
    return Quiz.objects.filter(external_user=external_user).order_by("-created_at")


@router.get("/quizzes/{quiz_id}", response=QuizRequestOutSchema, by_alias=True)
def get_quiz_request_by_id(request, quiz_id: int) -> QuizRequestOutSchema:
    external_user = get_existing_external_user(request)
    try:
        quiz_request = Quiz.objects.get(id=quiz_id, external_user=external_user)
    except Quiz.DoesNotExist:
        raise HttpError(404, "Quiz request not found.")
    return quiz_request


@router.post(
    "/solutions",
    response=SolutionResponseSchema,
    tags=["Solution"],
    by_alias=True,
    deprecated=True,
)
def question_solution_endpoint(request, payload: SolutionRequestSchema) -> Dict:
    solution = generate_solution(payload.question, payload.solution_level)
    QuizSolution.objects.create(**payload.dict(), user_id=request.auth.get("userId"))
    return solution


@router.get(
    "/solutions",
    response=List[SolutionRequestOutSchema],
    tags=["Solution"],
    by_alias=True,
    deprecated=True,
)
@paginate(PageNumberPagination, page_size=10, max_page_size=50)
def get_all_solution_request(request) -> Dict:
    user_id = request.auth.get("userId")
    if not user_id:
        raise HttpError(401, "Authentication required.")
    return QuizSolution.objects.filter(user_id=user_id).order_by("-created_at")


@router.get(
    "/solutions/{solution_id}",
    response=SolutionRequestOutSchema,
    tags=["Solution"],
    by_alias=True,
    deprecated=True,
)
def get_solution_request_by_id(request, solution_id: int) -> SolutionRequestOutSchema:
    user_id = request.auth.get("userId")
    if not user_id:
        raise HttpError(401, "Unauthorized")
    try:
        solution_request = QuizSolution.objects.get(id=solution_id, user_id=user_id)
    except QuizSolution.DoesNotExist:
        raise HttpError(404, "Solution request not found.")
    return solution_request


@router.get("/config", response=Dict[str, List], by_alias=True, tags=["Config"])
def get_quiz_config(request) -> Dict:
    question_types = [{"id": qt.value, "name": qt.label} for qt in QuestionType]
    difficulty_levels = [{"id": dl.value, "name": dl.label} for dl in DifficultyLevels]
    limits = [{"id": limit.value, "name": str(limit.value)} for limit in Limits]

    return {
        "questionTypes": question_types,
        "difficultyLevels": difficulty_levels,
        "limits": limits,
    }


@router.post("/uploads", response=UploadSuccess, tags=["Upload"], by_alias=True)
def upload_file(request, file: File[UploadedFile] = None):
    if not file:
        raise HttpError(400, "No file uploaded.")
    if file.content_type != "text/plain":
        raise HttpError(415, "Invalid file type. Only text files are allowed.")
    if file.size > 5 * 1024 * 1024:
        raise HttpError(413, "File size exceeds the limit of 5MB.")

    return {
        "filename": file.name,
        "size": file.size,
        "message": "File uploaded successfully",
    }
