import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField


class QuestionType(models.TextChoices):
    SINGLE = 'Single'
    MULTI = 'Multi'
    FILL_IN_THE_BLANC= 'Fill'
    ORDER = 'Order'


class QuizRequest(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    question_count = models.IntegerField()
    difficulty = models.IntegerField()
    question_type = ArrayField(models.CharField(max_length=100, choices=QuestionType.choices), blank=False)
    content = models.CharField(max_length=500)
