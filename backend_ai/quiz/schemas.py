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

class MultiChoiceQuestionSchema(BaseQuestionSchema):
    options: List[str]
    correct_answer: List[str]

class SingleChoiceQuestionSchema(BaseQuestionSchema):
    options: List[str]
    correct_answer: str


class FillInTheBlankQuestion(BaseQuestionSchema):
    correct_answer: List[str]


class OrderingQuestionSchema(BaseQuestionSchema):
    options: List[str]
    correct_order: List[str]


class QuizResponseSchema(Schema):
    questions: List[Union[OrderingQuestionSchema, FillInTheBlankQuestion, SingleChoiceQuestionSchema, MultiChoiceQuestionSchema]]


class SolutionSchema(Schema):
    text: str