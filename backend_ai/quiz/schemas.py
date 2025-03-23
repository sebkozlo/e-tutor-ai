from enum import Enum
from ninja import Schema
from typing import List, Union


class QuestionType(str, Enum):
    single = 'single'
    multi = 'multi'
    fill_in_the_blank = 'fill'
    ordering = 'ordering'


class QuizRequestSchema(Schema):
    question_count: int
    difficulty: int
    question_type: List[QuestionType]
    content: str


class BaseQuestionSchema(Schema):
    question: str
    question_type: str
    options: List[str]
    correct_answer: List[str]


class QuizResponseSchema(Schema):
    questions: List[BaseQuestionSchema]


class SolutionRequestSchema(BaseQuestionSchema):
    question: str
    solution_level: int = 1

class SolutionResponseSchema(Schema):
    solution: str

