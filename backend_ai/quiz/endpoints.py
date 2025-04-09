from ninja import Router
from .schemas import QuizRequestSchema, SolutionResponseSchema, QuizResponseListSchema
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
    # QuizRequest.objects.create(**payload.dict())
    # QuizResponseSchema.objects.create(**quiz)
    return quiz


# @router.post("/solution", response=SolutionResponseSchema, tags=['Quiz'])
# def question_solution_endpoint(request, payload: SolutionRequestSchema):
#     solution = generate_solution(payload.question, payload.solution_level)
#     return solution