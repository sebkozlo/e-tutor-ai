from ninja import Router
from .schemas import QuizRequestSchema, QuizResponseSchema, SolutionResponseSchema, SolutionRequestSchema
from .utils import generate_quiz, generate_solution


router = Router()

@router.post("/generate", response=QuizResponseSchema, tags=['Quiz'])
def generate_quiz_endpoint(request, payload: QuizRequestSchema):
    quiz = generate_quiz(payload.question_count, payload.difficulty, payload.question_type, payload.content)
    return quiz


@router.post("/solution", response=SolutionResponseSchema, tags=['Quiz'])
def question_solution_endpoint(request, payload: SolutionRequestSchema):
    solution = generate_solution(payload.question, payload.solution_level)
    return solution