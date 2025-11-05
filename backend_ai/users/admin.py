from django.contrib import admin
from .models import ExternalUser


@admin.register(ExternalUser)
class ExternalUser(admin.ModelAdmin):
    list_display = ["id", "external_id", "email", "created_at"]
    search_fields = ["external_id", "email"]
    readonly_fields = ["external_id", "email", "created_at"]
    fields = ["external_id", "email", "stripe_customer_id", "created_at"]
    ordering = ["-created_at"]
