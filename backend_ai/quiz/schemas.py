from enum import Enum
from ninja import Schema
from ninja import ModelSchema

from .models import QuizRequest, Question
from typing import List


def to_camel(string: str) -> str:
    parts = string.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])


class CamelModelSchema(Schema):
    str_field_name: str
    float_field_name: float

    class Config(Schema.Config):
        alias_generator = to_camel


class QuizRequestSchema(ModelSchema):
    class Config(Schema.Config):
        model = QuizRequest
        model_fields = ["question_count", "difficulty", "question_type", "content"]
        alias_generator = to_camel
        populate_by_name = True


# class BaseQuestionSchema(ModelSchema):
#     class Config(Schema.Config):
#         model = Question
#         model_fields = ["question", "question_type", "options", "correct_answer"]
#         alias_generator = to_camel
#         populate_by_name = True

class BaseQuestionSchema(Schema):
    question: str
    question_type: str
    options: List[str]
    correct_answer: List[str]


class QuizResponseSchema(Schema):
    id: str
    questions: List[BaseQuestionSchema]

    class Config(Schema.Config):
        alias_generator = to_camel


class SolutionRequestSchema(BaseQuestionSchema):
    question: str
    solutionLevel: int = 1


class SolutionResponseSchema(Schema):
    solution: str

