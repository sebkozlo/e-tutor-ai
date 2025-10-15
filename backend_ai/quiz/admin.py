from django.contrib import admin
from .models import Quiz, QuizSolution


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "external_user",
        "question_count",
        "difficulty",
        "question_type",
        "content",
        "created_at",
        "token_usage__total_tokens",
    ]
    search_fields = ["question_type", "content"]
    list_filter = ["difficulty", "created_at"]


@admin.register(QuizSolution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ["id", "external_user", "question", "solution_level", "created_at"]
