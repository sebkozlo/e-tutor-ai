from django.contrib import admin
from .models import TokenUsage, TokenLimit


@admin.register(TokenUsage)
class TokenUsageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "external_user",
        "input_tokens",
        "output_tokens",
        "total_tokens",
        "created_at",
    ]
    search_fields = ["external_user__email"]
    list_filter = ["created_at"]


@admin.register(TokenLimit)
class TokenLimitAdmin(admin.ModelAdmin):
    list_display = [
        "period",
        "limit",
        "subscription_plan__name",
        "subscription_plan__price",
    ]
    search_fields = ["period"]
