from django.db import models, transaction
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from core.enums import DifficultyLevels, QuestionType, SolutionLevels, Limits
from users.models import ExternalUser
from tokens.models import TokenUsage


class QuizManager(models.Manager):
    def create_with_token_usage(
        self,
        external_user,
        question_count,
        difficulty,
        question_type,
        content,
        usage_data,
    ):
        with transaction.atomic():
            token_usage = TokenUsage.objects.create(
                external_user=external_user,
                input_tokens=usage_data["input_tokens"],
                output_tokens=usage_data["output_tokens"],
                total_tokens=usage_data["total_tokens"],
            )
            return self.create(
                external_user=external_user,
                question_count=question_count,
                difficulty=difficulty,
                question_type=question_type,
                content=content,
                token_usage=token_usage,
            )


class Quiz(models.Model):
    id = models.BigAutoField(primary_key=True)
    external_user = models.ForeignKey(
        ExternalUser, on_delete=models.CASCADE, related_name="quizzes"
    )
    token_usage = models.ForeignKey(
        TokenUsage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="token_usages",
    )
    question_count = models.IntegerField(
        validators=[
            MinValueValidator(Limits.MIN_QUESTIONS),
            MaxValueValidator(Limits.MAX_QUESTIONS),
        ]
    )
    difficulty = models.CharField(max_length=10, choices=DifficultyLevels.choices)
    question_type = ArrayField(
        models.CharField(max_length=100, choices=QuestionType.choices), blank=False
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = QuizManager()

    class Meta:
        indexes = [
            models.Index(fields=["external_user"]),
            models.Index(fields=["-created_at"]),
        ]


class QuizSolution(models.Model):
    id = models.BigAutoField(primary_key=True)
    external_user = models.ForeignKey(
        ExternalUser, on_delete=models.CASCADE, related_name="quiz_solutions"
    )
    question = models.TextField()
    solution_level = models.IntegerField(choices=SolutionLevels.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["external_user"]),
            models.Index(fields=["-created_at"]),
        ]
