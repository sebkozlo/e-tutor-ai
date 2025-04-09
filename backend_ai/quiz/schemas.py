from ninja import Schema
from ninja import ModelSchema
from typing import List
from .models import QuizRequest


def to_camel(string: str) -> str:
    parts = string.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])


class QuizResponseSchema(Schema):
    question: str
    question_type: str
    options: List[str]
    correct_answer: List[str]

    model_config = {
        "alias_generator": to_camel,
        "populate_by_name": True
    }


class QuizRequestSchema(ModelSchema):

    class Config:
        model = QuizRequest
        model_fields = ["user_id", "question_count", "difficulty", "question_type", "content"]
        alias_generator = to_camel
        populate_by_name = True


class QuizResponseListSchema(Schema):
    questions: List[QuizResponseSchema]


class SolutionRequestSchema(Schema):
    question: str
    solutionLevel: int = 1


class SolutionResponseSchema(Schema):
    solution: str

