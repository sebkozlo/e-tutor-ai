from ninja import Router
from .schemas import QuizRequestSchema, QuizResponseSchema, SolutionSchema
from .utils import generate_quiz, question_solution

router = Router()

@router.post("/generate", response=QuizResponseSchema, tags=['Quiz'])
def generate_quiz_endpoint(request, payload: QuizRequestSchema):
    quiz = generate_quiz(payload.question_count, payload.difficulty, payload.question_type, payload.content)
    return quiz

@router.post("/solution", response=SolutionSchema, tags=['Quiz'])
def question_solution_endpoint(request, payload: SolutionSchema):
    solution = question_solution(payload.question)
    return solution