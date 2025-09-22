import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator


class QuestionType(models.TextChoices):
    SINGLE = "SINGLE"
    MULTI = "MULTI"
    FILL_IN_THE_BLANC = "FILL"
    ORDER = "ORDER"
    TRUE_FSALSE = "TRUE_FALSE"


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


class Quiz(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    question_count = models.IntegerField(validators=[MinValueValidator(Limits.MIN_QUESTIONS), MaxValueValidator(Limits.MAX_QUESTIONS)])
    difficulty = models.CharField(max_length=10, choices=DifficultyLevels.choices)
    question_type = ArrayField(
        models.CharField(max_length=100, choices=QuestionType.choices), blank=False
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['-created_at']),
        ]

class QuizSolution(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    question = models.TextField()
    solution_level = models.IntegerField(choices=SolutionLevels)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['-created_at']),
        ]