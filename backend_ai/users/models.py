from django.db import models
import uuid


class ExternalUser(models.Model):
    id = models.AutoField(primary_key=True)
    external_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    email = models.EmailField(unique=True)
    stripe_customer_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.external_id)

    def create_or_get_stripe_customer(self):
        if not self.stripe_customer_id:
            import stripe
            from django.conf import settings

            stripe.api_key = settings.STRIPE_SECRET_KEY

            stripe_customer = stripe.Customer.create(
                email=self.email, metadata={"external_user_id": self.id}
            )
            self.stripe_customer_id = stripe_customer.id
            self.save()
        return self
