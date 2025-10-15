from django.db import models
from core.models import ExternalUser


class Customer(models.Model):
    external_user = models.OneToOneField(
        ExternalUser, on_delete=models.CASCADE, related_name="customer"
    )
    stripe_customer_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True
    )
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
