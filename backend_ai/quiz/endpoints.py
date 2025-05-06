from ninja import Router
from .schemas import QuizRequestSchema, SolutionResponseSchema, QuizResponseListSchema, SolutionRequestSchema, SolutionRequest
from .utils import generate_quiz, generate_solution
from .models import QuizRequest


router = Router()

@router.post("/generate",  response=QuizResponseListSchema, tags=['Quiz'], by_alias=True)
def generate_quiz_endpoint(request, payload: QuizRequestSchema):
    quiz = generate_quiz(
        payload.question_count,
        payload.difficulty,
        payload.question_type,
        payload.content
    )
    QuizRequest.objects.create(**payload.dict())
    return quiz


@router.post("/solution", response=SolutionResponseSchema, tags=['Quiz'])
def question_solution_endpoint(request, payload: SolutionRequestSchema):
    solution = generate_solution(payload.question, payload.solution_level)
    SolutionRequest.objects.create(**payload.dict())
    return solution


@router.get("/all_quiz_request", response=QuizRequestSchema)
def get_all_quiz_request(request):
    qs = QuizRequest.objects.all()
    return qs

@router.get("/all_solution_request", response=SolutionRequestSchema, by_alias=True)
def get_all_solution_request(request):
    qs = SolutionRequest.objects.all()
    return qs