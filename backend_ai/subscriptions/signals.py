from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import ExternalUser
from .models import Subscription, SubscriptionPlan


@receiver(post_save, sender=ExternalUser)
def create_free_subscription(sender, instance, created, **kwargs):
    if created:
        try:
            free_plan = SubscriptionPlan.objects.get(name="Free", is_free=True)
            Subscription.objects.create(
                external_user=instance, plan=free_plan, status="active"
            )
        except SubscriptionPlan.DoesNotExist:
            pass
