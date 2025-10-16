from django.db import models
from core.models import ExternalUser
from django.utils import timezone
from core.enums import PeriodicChoices
from django.db.models import Q


class TokenUsage(models.Model):
    external_user = models.ForeignKey(
        ExternalUser, on_delete=models.CASCADE, related_name="token_usages"
    )
    input_tokens = models.IntegerField(default=0)
    output_tokens = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_usage_since(cls, external_user, start_time, limit=None):
        result = cls.objects.filter(
            external_user=external_user, created_at__gte=start_time
        ).aggregate(
            total=models.Sum(models.F("input_tokens") + models.F("output_tokens"))
        )
        return result["total"] or 0

    @classmethod
    def get_day_usage(cls, external_user, limit=None):
        start_of_day = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return cls.get_usage_since(external_user, start_of_day, limit)

    @classmethod
    def get_week_usage(cls, external_user, limit=None):
        today = timezone.now()
        start_of_week = today - timezone.timedelta(days=today.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        return cls.get_usage_since(external_user, start_of_week, limit)

    @classmethod
    def get_month_usage(cls, external_user, limit=None):
        start_of_month = timezone.now().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        return cls.get_usage_since(external_user, start_of_month, limit)

    @classmethod
    def check_limit(cls, external_user, period):
        usage_method = {
            PeriodicChoices.DAY: cls.get_day_usage,
            PeriodicChoices.WEEK: cls.get_week_usage,
            PeriodicChoices.MONTH: cls.get_month_usage,
        }
        usage = usage_method[period](external_user)

        plan = external_user.subscription.plan
        print(plan)
        limit_obj = (
            TokenLimit.objects.filter(period=period)
            .filter(Q(subscription_plan=plan) | Q(subscription_plan=None))
            .order_by("-subscription_plan")
            .first()
        )

        if limit_obj:
            limit = limit_obj.limit
            exceeded = usage > limit
        else:
            limit = None
            exceeded = False

        subscription_plan_name = plan.name

        return usage, limit, exceeded, subscription_plan_name


class TokenLimit(models.Model):
    subscription_plan = models.ForeignKey(
        "subscriptions.SubscriptionPlan",
        on_delete=models.CASCADE,
        related_name="token_limits",
        null=True,
        blank=True,
    )
    period = models.CharField(max_length=10, choices=PeriodicChoices.choices)
    limit = models.IntegerField(default=1000)

    class Meta:
        verbose_name = "Token Limit"
        verbose_name_plural = "Token Limits"
        unique_together = [["subscription_plan", "period"]]

    def __str__(self):
        plan_name = self.subscription_plan.name if self.subscription_plan else "Default"
        return f"{plan_name} - {self.get_period_display()}: {self.limit}"
