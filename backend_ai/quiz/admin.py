from django.contrib import admin
from .models import QuizRequest, SolutionRequest
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class QuizRequestResource(resources.ModelResource):
    class Meta:
        model = QuizRequest
        fields = (
            "id",
            "user_id",
            "question_count",
            "difficulty",
            "question_type",
            "content",
        )


class QuizRequestAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = [
        "id",
        "user_id",
        "question_count",
        "difficulty",
        "question_type",
        "content",
    ]
    search_fields = ["question_type", "content"]


class SolutionRequestAdmin(admin.ModelAdmin):
    list_display = ["id", "user_id", "question", "solution_level"]


admin.site.register(QuizRequest, QuizRequestAdmin)
admin.site.register(SolutionRequest, SolutionRequestAdmin)
