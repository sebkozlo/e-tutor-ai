from datetime import datetime, timezone
from typing import Optional

import stripe

from django.conf import settings

from core.enums import SubscriptionStatusChoices
from payments.models import PaymentRecord
from subscriptions.models import SubscriptionPlan, Subscription
from users.models import ExternalUser

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    @staticmethod
    def _timestamp_to_datetime(ts: Optional[int]) -> Optional[datetime]:
        if ts is None:
            return None
        return datetime.fromtimestamp(ts, tz=timezone.utc)

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
                "external_user_id": str(external_user.id),
                "plan_id": str(plan.id),
            },
            subscription_data={
                "metadata": {
                    "external_user_id": str(external_user.id),
                    "plan_id": str(plan.id),
                }
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

        current_period_start = None
        current_period_end = None

        try:
            stripe_sub = stripe.Subscription.retrieve(stripe_subscription_id)

            if stripe_sub.get("items") and stripe_sub["items"].get("data"):
                first_item = stripe_sub["items"]["data"][0]

                current_period_start = StripeService._timestamp_to_datetime(
                    first_item.get("current_period_start")
                )
                current_period_end = StripeService._timestamp_to_datetime(
                    first_item.get("current_period_end")
                )

        except Exception:
            pass

        subscription, created = Subscription.objects.get_or_create(
            external_user=external_user,
            defaults={
                "plan": plan,
                "status": SubscriptionStatusChoices.ACTIVE,
                "stripe_subscription_id": stripe_subscription_id,
                "current_period_start": current_period_start,
                "current_period_end": current_period_end,
            },
        )

        if not created:
            subscription.plan = plan
            subscription.stripe_subscription_id = stripe_subscription_id
            subscription.status = SubscriptionStatusChoices.ACTIVE
            subscription.current_period_start = current_period_start
            subscription.current_period_end = current_period_end

        subscription.save()

        PaymentRecord.objects.create(
            external_user=external_user,
            event_type="checkout.session.completed",
            status=event_object.get("payment_status"),
            amount=event_object.get("amount_total"),
            currency=event_object.get("currency"),
            stripe_customer_id=customer_id,
            stripe_subscription_id=stripe_subscription_id,
            stripe_session_id=event_object.get("id"),
            raw=event_object,
        )

    @staticmethod
    def handle_subscription_cancelled(subscription_data: dict) -> None:
        stripe_subscription_id = subscription_data.get("id")
        if not stripe_subscription_id:
            return

        try:
            subscription = Subscription.objects.get(
                stripe_subscription_id=stripe_subscription_id
            )
        except Subscription.DoesNotExist:
            return

        current_period_start = StripeService._timestamp_to_datetime(
            subscription_data.get("current_period_start")
        )
        current_period_end = StripeService._timestamp_to_datetime(
            subscription_data.get("current_period_end")
        )

        subscription.status = SubscriptionStatusChoices.CANCELED
        subscription.cancel_at_period_end = subscription_data.get("cancel_at_period_end", False)

        if current_period_start:
            subscription.current_period_start = current_period_start
        if current_period_end:
            subscription.current_period_end = current_period_end

        subscription.save()

    @staticmethod
    def handle_subscription_updated(subscription_data: dict) -> None:
        stripe_subscription_id = subscription_data.get("id")
        if not stripe_subscription_id:
            return

        try:
            subscription = Subscription.objects.get(
                stripe_subscription_id=stripe_subscription_id
            )
        except Subscription.DoesNotExist:
            return

        stripe_status = subscription_data.get("status")
        if stripe_status == "active":
            subscription.status = SubscriptionStatusChoices.ACTIVE
        elif stripe_status == "canceled":
            subscription.status = SubscriptionStatusChoices.CANCELED
        elif stripe_status == "past_due":
            subscription.status = SubscriptionStatusChoices.PAST_DUE
        elif stripe_status == "unpaid":
            subscription.status = SubscriptionStatusChoices.UNPAID

        subscription.cancel_at_period_end = subscription_data.get(
            "cancel_at_period_end", False
        )

        subscription.current_period_start = StripeService._timestamp_to_datetime(
            subscription_data.get("current_period_start")
        )
        subscription.current_period_end = StripeService._timestamp_to_datetime(
            subscription_data.get("current_period_end")
        )

        subscription.save()

    @staticmethod
    def handle_payment_succeeded(invoice_data: dict) -> None:
        stripe_subscription_id = invoice_data.get("subscription")
        if not stripe_subscription_id:
            return

        try:
            subscription = Subscription.objects.get(
                stripe_subscription_id=stripe_subscription_id
            )
        except Subscription.DoesNotExist:
            return

        subscription.status = SubscriptionStatusChoices.ACTIVE
        subscription.current_period_start = StripeService._timestamp_to_datetime(
            invoice_data.get("period_start")
        )
        subscription.current_period_end = StripeService._timestamp_to_datetime(
            invoice_data.get("period_end")
        )
        subscription.save()

        PaymentRecord.objects.create(
            external_user=subscription.external_user,
            event_type="invoice.payment_succeeded",
            status="paid",
            amount=invoice_data.get("amount_paid"),
            currency=invoice_data.get("currency"),
            stripe_customer_id=invoice_data.get("customer"),
            stripe_subscription_id=stripe_subscription_id,
            stripe_invoice_id=invoice_data.get("id"),
            raw=invoice_data,
        )

    @staticmethod
    def handle_payment_failed(invoice_data: dict) -> None:
        stripe_subscription_id = invoice_data.get("subscription")
        if not stripe_subscription_id:
            return

        try:
            subscription = Subscription.objects.get(
                stripe_subscription_id=stripe_subscription_id
            )
        except Subscription.DoesNotExist:
            return

        subscription.status = SubscriptionStatusChoices.PAST_DUE
        subscription.save()

        PaymentRecord.objects.create(
            external_user=subscription.external_user,
            event_type="invoice.payment_failed",
            status="failed",
            amount=invoice_data.get("amount_due"),
            currency=invoice_data.get("currency"),
            stripe_customer_id=invoice_data.get("customer"),
            stripe_subscription_id=stripe_subscription_id,
            stripe_invoice_id=invoice_data.get("id"),
            raw=invoice_data,
        )
