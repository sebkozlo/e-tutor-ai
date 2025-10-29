from django.conf import settings
from typing import Optional
import stripe

from users.models import ExternalUser
from subscriptions.models import SubscriptionPlan, Subscription
from payments.models import PaymentRecord
from core.enums import SubscriptionStatusChoices


stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    @staticmethod
    def get_or_create_customer(external_user: ExternalUser) -> str:
        if external_user.stripe_customer_id:
            return external_user.stripe_customer_id

        customer = stripe.Customer.create(
            email=external_user.email,
            metadata={"external_user_id": external_user.id},
        )
        external_user.stripe_customer_id = customer.id
        external_user.save()
        return customer.id

    @staticmethod
    def create_checkout_session(
        external_user: ExternalUser,
        plan: SubscriptionPlan,
        success_url: str,
        cancel_url: str,
    ) -> stripe.checkout.Session:
        customer_id = StripeService.get_or_create_customer(external_user)

        session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=["card"],
            line_items=[
                {
                    "price": plan.stripe_price_id,
                    "quantity": 1,
                }
            ],
            mode="subscription",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                "external_user_id": external_user.id,
                "plan_id": plan.id,
            },
        )
        return session

    @staticmethod
    def handle_checkout_completed(event_object: dict) -> None:
        customer_id = event_object.get("customer")
        stripe_subscription_id = event_object.get("subscription")
        metadata = event_object.get("metadata") or {}

        external_user_id = metadata.get("external_user_id")
        plan_id = metadata.get("plan_id")

        if not (
            customer_id and stripe_subscription_id and external_user_id and plan_id
        ):
            return

        try:
            external_user = ExternalUser.objects.get(id=external_user_id)
        except ExternalUser.DoesNotExist:
            return

        if not external_user.stripe_customer_id:
            external_user.stripe_customer_id = customer_id
            external_user.save()

        try:
            plan = SubscriptionPlan.objects.get(id=plan_id)
        except SubscriptionPlan.DoesNotExist:
            return

        subscription, _ = Subscription.objects.get_or_create(
            external_user=external_user,
            defaults={"plan": plan, "status": SubscriptionStatusChoices.ACTIVE},
        )

        subscription.plan = plan
        subscription.stripe_subscription_id = stripe_subscription_id
        subscription.status = SubscriptionStatusChoices.ACTIVE

        try:
            stripe_sub = stripe.Subscription.retrieve(stripe_subscription_id)
            if stripe_sub and stripe_sub.get("current_period_start"):
                from datetime import datetime, timezone

                def ts_to_dt(ts: Optional[int]):
                    if ts is None:
                        return None
                    return datetime.fromtimestamp(ts, tz=timezone.utc)

                subscription.current_period_start = ts_to_dt(
                    stripe_sub.get("current_period_start")
                )
            if stripe_sub and stripe_sub.get("current_period_end"):
                from datetime import datetime, timezone

                subscription.current_period_end = datetime.fromtimestamp(
                    stripe_sub.get("current_period_end"), tz=timezone.utc
                )
        except Exception:
            pass

        subscription.save()

        PaymentRecord.objects.create(
            external_user=external_user,
            event_type="checkout.session.completed",
            status=event_object.get("status"),
            amount=event_object.get("amount"),
            currency=event_object.get("currency"),
            stripe_customer_id=customer_id,
            stripe_subscription_id=stripe_subscription_id,
            stripe_session_id=event_object.get("id"),
            raw=event_object,
        )
