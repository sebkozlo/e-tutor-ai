from django.db import models
from django.utils import timezone
from core.models import ExternalUser
from core.enums import SubscriptionStatusChoices, SubscriptionIntervalChoices


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    stripe_product_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True
    )
    stripe_price_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default="PLN")
    interval = models.CharField(
        max_length=10,
        choices=SubscriptionIntervalChoices.choices,
        default=SubscriptionIntervalChoices.MONTH,
    )

    is_active = models.BooleanField(default=True)
    is_free = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["price"]

    def __str__(self):
        return f"{self.name} - {self.price} {self.currency} / {self.interval}"


class Subscription(models.Model):
    external_user = models.OneToOneField(
        ExternalUser, on_delete=models.CASCADE, related_name="subscription"
    )
    plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.PROTECT, related_name="subscriptions"
    )
    stripe_subscription_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=SubscriptionStatusChoices.choices,
        default=SubscriptionStatusChoices.ACTIVE,
    )
    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    cancel_at_period_end = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Subscription of {self.external_user.email} - {self.plan.name} ({self.status})"

    @property
    def is_active(self):
        return self.status in [
            SubscriptionStatusChoices.ACTIVE,
            SubscriptionStatusChoices.TRIALING,
        ]
