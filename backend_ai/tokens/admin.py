from django.contrib import admin
from .models import TokenUsage, TokenBalance


class TokenBalanceAdmin(admin.ModelAdmin):
    list_display = ["external_user", "balance"]
    search_fields = ["external_user__email"]


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


admin.site.register(TokenBalance, TokenBalanceAdmin)
admin.site.register(TokenUsage, TokenUsageAdmin)
