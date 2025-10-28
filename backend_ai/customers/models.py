from django.db import models
from core.models import ExternalUser
from django.conf import settings
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


class Customer(models.Model):
    external_user = models.OneToOneField(
        ExternalUser, on_delete=models.CASCADE, related_name="customer"
    )
    stripe_customer_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def email(self):
        return self.external_user.email

    def __str__(self):
        return self.email

    @classmethod
    def create_stripe_customer(cls, external_user: ExternalUser):

        customer = cls.objects.get(
            external_user=external_user,
            defaults={'email': external_user.email}
        )

        if not customer.stripe_customer_id:
            stripe_customer = stripe.Customer.create(
                email=customer.email,
                metadata={'external_user_id': external_user.id}
            )
            customer.stripe_customer_id = stripe_customer.id
            customer.save()
        else:
            stripe_customer = stripe.Customer.retrieve(customer.stripe_customer_id)
        return customer
