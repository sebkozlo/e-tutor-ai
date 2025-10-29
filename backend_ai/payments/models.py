from django.db import models


class Tier(models.TextChoices):
    FREE = "FREE"
    BASIC = "BASIC"
    PREMIUM = "PREMIUM"
    ENTERPRISE = "ENTERPRISE"


class Plan(models.Model):
    name = models.CharField(max_length=50, choices=Tier.choices, unique=True)
    monthly_token_limit = models.IntegerField()
    daily_token_limit = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name


class PaymentRecord(models.Model):
    external_user = models.ForeignKey(
        "users.ExternalUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payment_records",
    )

    event_type = models.CharField(max_length=64)
    status = models.CharField(max_length=32, null=True, blank=True)

    amount = models.IntegerField(null=True, blank=True)
    currency = models.CharField(max_length=10, null=True, blank=True)

    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_subscription_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_payment_intent_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_invoice_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_session_id = models.CharField(max_length=255, null=True, blank=True)

    raw = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.event_type} | {self.status or '-'} | {self.stripe_session_id or self.stripe_payment_intent_id or self.stripe_invoice_id or self.stripe_subscription_id or 'n/a'}"
