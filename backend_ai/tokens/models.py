from django.db import models
from core.models import ExternalUser


class TokenBalance(models.Model):
    external_user = models.ForeignKey(
        ExternalUser, on_delete=models.CASCADE, related_name="token_balances"
    )
    balance = models.IntegerField(default=0)


class TokenUsage(models.Model):
    external_user = models.ForeignKey(
        ExternalUser, on_delete=models.CASCADE, related_name="token_usages"
    )
    input_tokens = models.IntegerField(default=0)
    output_tokens = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def day_usage(self):
        from django.utils import timezone
        from datetime import timedelta

        start_of_day = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return (
            TokenUsage.objects.filter(
                external_user=self.external_user, created_at__gte=start_of_day
            ).aggregate(models.Sum("total_tokens"))["total_tokens__sum"]
            or 0
        )
