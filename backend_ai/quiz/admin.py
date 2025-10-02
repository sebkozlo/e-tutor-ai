from django.contrib import admin
from .models import Quiz, QuizSolution
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class QuizRequestResource(resources.ModelResource):
    class Meta:
        model = Quiz
        fields = (
            "id",
            "external_user",
            "question_count",
            "difficulty",
            "question_type",
            "content",
            "created_at",
        )


class QuizRequestAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = [
        "id",
        "external_user",
        "question_count",
        "difficulty",
        "question_type",
        "content",
        "created_at",
    ]
    search_fields = ["question_type", "content"]


class SolutionRequestAdmin(admin.ModelAdmin):
    list_display = ["id", "external_user", "question", "solution_level", "created_at"]


admin.site.register(Quiz, QuizRequestAdmin)
admin.site.register(QuizSolution, SolutionRequestAdmin)
