import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField


class QuestionType(models.TextChoices):
    SINGLE = "SINGLE"
    MULTI = "MULTI"
    FILL_IN_THE_BLANC = "FILL"
    ORDER = "ORDER"


class QuizRequest(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    question_count = models.IntegerField()
    difficulty = models.IntegerField()
    question_type = ArrayField(
        models.CharField(max_length=100, choices=QuestionType.choices), blank=False
    )
    content = models.CharField(max_length=500)


class SolutionRequest(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=1000)
    solution_level = models.IntegerField()
