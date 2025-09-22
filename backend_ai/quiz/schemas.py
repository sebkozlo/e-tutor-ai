from ninja import Schema
from ninja import ModelSchema
from typing import List, Optional
from .models import Quiz, QuizSolution


def to_camel(string: str) -> str:
    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


class ChoiceSchema(Schema):
    id: str
    name: str


class QuizResponseSchema(Schema):
    question: str
    question_type: str
    options: List[str]
    correct_answer: List[str]

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class QuizRequestSchema(ModelSchema):
    class Config:
        model = Quiz
        model_fields = [
            "question_count",
            "difficulty",
            "question_type",
            "content",
        ]
        file: Optional = None
        alias_generator = to_camel
        populate_by_name = True


class QuizRequestOutSchema(ModelSchema):
    class Config:
        model = Quiz
        model_fields = [
            "id",
            "user_id",
            "question_count",
            "difficulty",
            "question_type",
            "content",
            "created_at",
        ]
        alias_generator = to_camel
        populate_by_name = True


class QuizResponseListSchema(Schema):
    questions: List[QuizResponseSchema]


class SolutionRequestSchema(ModelSchema):
    class Config:
        model = QuizSolution
        model_fields = ["question", "solution_level"]
        alias_generator = to_camel
        populate_by_name = True


class SolutionResponseSchema(Schema):
    solution: str


class SolutionRequestOutSchema(ModelSchema):
    class Config:
        model = QuizSolution
        model_fields = ["id", "user_id", "question", "solution_level", "created_at"]
        alias_generator = to_camel
        populate_by_name = True


class UploadSuccess(Schema):
    filename: str
    size: int
    message: str


class ErrorResponse(Schema):
    detail: str
