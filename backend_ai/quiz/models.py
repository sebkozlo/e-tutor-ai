import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField


class QuestionType(models.TextChoices):
    SINGLE = "SINGLE"
    MULTI = "MULTI"
    FILL_IN_THE_BLANC = "FILL"
    ORDER = "ORDER"


class DifficultyLevels(models.TextChoices):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    EXPERT = "EXPERT"
    MASTER = "MASTER"


class Limits(models.IntegerChoices):
    MIN_QUESTIONS = 1
    MAX_QUESTIONS = 50


class QuizRequest(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    question_count = models.IntegerField()
    difficulty = models.IntegerField()
    question_type = ArrayField(
        models.CharField(max_length=100, choices=QuestionType.choices), blank=False
    )
    content = models.CharField(max_length=500)


class SolutionRequest(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=1000)
    solution_level = models.IntegerField()
