from django.contrib import admin
from .models import PaymentRecord


@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at",
        "event_type",
        "status",
        "external_user",
        "external_user__email",
        "amount",
        "currency",
        "stripe_session_id",
        "stripe_invoice_id",
    )
    list_filter = ("event_type", "status", "currency")
    search_fields = (
        "stripe_customer_id",
        "stripe_subscription_id",
        "stripe_payment_intent_id",
        "stripe_invoice_id",
        "stripe_session_id",
        "external_user__email",
    )
    ordering = ("-created_at",)
