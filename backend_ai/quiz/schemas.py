from ninja import Schema
from ninja import ModelSchema
from typing import List, Optional
from pydantic import Field
from .models import Quiz, QuizSolution, DifficultyLevels, QuestionType
from core.utils import to_camel


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
    difficulty: DifficultyLevels = Field(..., example="EASY")
    question_type: List[QuestionType] = Field(..., example=["SINGLE", "MULTI"])
    question_count: int = Field(..., example=5)
    content: str = Field(..., example="Python programing language")

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
            "external_user",
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
        model_fields = [
            "id",
            "external_user",
            "question",
            "solution_level",
            "created_at",
        ]
        alias_generator = to_camel
        populate_by_name = True


class UploadSuccess(Schema):
    filename: str
    size: int
    message: str


class TaskResponseSchema(Schema):
    status: str
    message: str
    data: Optional["QuizResponseListSchema"] = None
    quiz_id: Optional[int] = None
    error: Optional[str] = None
    task_id: Optional[str] = None
