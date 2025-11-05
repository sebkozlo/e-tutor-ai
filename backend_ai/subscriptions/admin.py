from django.contrib import admin
from django.utils.html import format_html
from .models import SubscriptionPlan, Subscription
from core.enums import SubscriptionStatusChoices


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "interval", "is_active", "subscriber_count"]
    list_filter = ["is_active", "is_free", "interval"]
    search_fields = ["name"]
    list_editable = ["is_active"]

    fields = (
        "name",
        "description",
        "price",
        "currency",
        "interval",
        "is_active",
        "is_free",
        "stripe_product_id",
        "stripe_price_id",
    )

    def subscriber_count(self, obj):
        return obj.subscriptions.filter(status=SubscriptionStatusChoices.ACTIVE).count()

    subscriber_count.short_description = "Active Users"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["external_user", "plan", "status_display", "current_period_end"]
    list_filter = ["status", "plan"]
    search_fields = ["external_user__email"]

    fields = (
        "external_user",
        "plan",
        "status",
        "current_period_start",
        "current_period_end",
        "cancel_at_period_end",
        "stripe_subscription_id",
    )

    def status_display(self, obj):
        colors = {
            SubscriptionStatusChoices.ACTIVE: "green",
            SubscriptionStatusChoices.TRIALING: "blue",
            SubscriptionStatusChoices.CANCELED: "red",
            SubscriptionStatusChoices.PAST_DUE: "orange",
            SubscriptionStatusChoices.UNPAID: "darkred",
            SubscriptionStatusChoices.INCOMPLETE: "purple",
            SubscriptionStatusChoices.INCOMPLETE_EXPIRED: "gray",
        }
        color = colors.get(obj.status, "black")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_display.short_description = "Status"
