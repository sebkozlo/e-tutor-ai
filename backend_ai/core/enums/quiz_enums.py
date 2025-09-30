from django.db import models


class QuestionType(models.TextChoices):
    SINGLE = "SINGLE"
    MULTI = "MULTI"
    FILL_IN_THE_BLANC = "FILL"
    ORDER = "ORDER"
    TRUE_FALSE = "TRUE_FALSE"


class DifficultyLevels(models.TextChoices):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    EXPERT = "EXPERT"
    MASTER = "MASTER"


class SolutionLevels(models.IntegerChoices):
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3


class Limits(models.IntegerChoices):
    MIN_QUESTIONS = 1
    MAX_QUESTIONS = 50
