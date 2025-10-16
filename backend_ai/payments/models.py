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
