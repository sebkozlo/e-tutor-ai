import stripe
from ninja import Router, Schema
from ninja.errors import HttpError
from django.http import HttpRequest
from django.conf import settings
from users.services.user_service import get_existing_external_user
from payments.services.stripe_service import StripeService
from core.enums import SubscriptionStatusChoices
from .schemas import (
    CheckoutRequest,
    CheckoutResponse,
    SubscriptionPlanSchema,
    SubscriptionSchema,
    ListSubscriptionPlansSchema,
)
from .models import SubscriptionPlan
from .models import Subscription


router = Router()


@router.get("/plans", response=ListSubscriptionPlansSchema, by_alias=True)
def list_subscription_plans(request):
    plans = SubscriptionPlan.objects.all()
    plan_list = [
        {
            "name": plan.name,
            "price": plan.price,
            "description": plan.description,
            "currency": plan.currency,
            "is_free": plan.is_free,
            "id": plan.id,
        }
        for plan in plans
    ]
    return {
        "active_plan_id": get_existing_external_user(request).subscription.plan.id,
        "plans": plan_list,
    }


@router.get("/plans/{plan_id}", response=SubscriptionPlanSchema, by_alias=True)
def get_subscription_plan(request, plan_id: int):
    try:
        plan = SubscriptionPlan.objects.get(id=plan_id)
    except SubscriptionPlan.DoesNotExist:
        raise HttpError(404, "Plan not found")

    return plan


@router.get("/active", response=SubscriptionSchema, by_alias=True)
def get_active_subscription(request):
    external_user = get_existing_external_user(request)
    try:
        subscription = Subscription.objects.get(external_user=external_user)
    except Subscription.DoesNotExist:
        raise HttpError(404, "No active subscription found")
    return subscription


@router.post("/checkout", response=CheckoutResponse)
def create_checkout_session_api(request: HttpRequest, payload: CheckoutRequest):
    external_user = get_existing_external_user(request)

    try:
        plan = SubscriptionPlan.objects.get(id=payload.plan_id, is_active=True)
    except SubscriptionPlan.DoesNotExist:
        raise HttpError(404, "Plan not found")

    if plan.is_free:
        raise HttpError(400, "Free plan does not require checkout")

    if external_user.subscription.plan == plan:
        raise HttpError(400, "You already have this subscription plan")

    try:
        session = StripeService.create_checkout_session(
            external_user=external_user,
            plan=plan,
            success_url=f"{settings.FRONTEND_URL}/dashboard/subscription?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.FRONTEND_URL}/dashboard/subscription",
        )

        if not session:
            raise HttpError(500, "Failed to create checkout session")
    except Exception as e:
        raise HttpError(500, "Error creating checkout session")

    return CheckoutResponse(url=session.url, session_id=session.id)


@router.post("/cancel", response={200: dict, 404: dict, 400: dict})
def cancel_subscription(request: HttpRequest):
    external_user = get_existing_external_user(request)

    try:
        subscription = Subscription.objects.get(external_user=external_user)
    except Subscription.DoesNotExist:
        raise HttpError(404, "No active subscription found")

    if subscription.status == SubscriptionStatusChoices.CANCELED:
        raise HttpError(400, "Subscription is already cancelled")

    if subscription.plan.is_free:
        raise HttpError(400, "Cannot cancel free plan")

    if not subscription.stripe_subscription_id:
        raise HttpError(400, "No Stripe subscription found")

    try:
        stripe.Subscription.modify(
            subscription.stripe_subscription_id,
            cancel_at_period_end=True
        )

        subscription.cancel_at_period_end = True
        subscription.save(update_fields=['cancel_at_period_end'])

        return {
            "message": "Subscription will be cancelled at the end of the billing period",
            "access_until": subscription.current_period_end.isoformat()
            if subscription.current_period_end
            else None,
        }

    except stripe.error.StripeError as e:
        raise HttpError(500, f"Failed to cancel subscription: {str(e)}")


@router.post("/reactivate", response={200: dict, 404: dict, 400: dict})
def reactivate_subscription(request: HttpRequest):
    external_user = get_existing_external_user(request)

    try:
        subscription = Subscription.objects.get(external_user=external_user)
    except Subscription.DoesNotExist:
        raise HttpError(404, "No subscription found")

    if not subscription.cancel_at_period_end:
        raise HttpError(400, "Subscription is not scheduled for cancellation")

    if subscription.status == SubscriptionStatusChoices.CANCELED:
        raise HttpError(
            400, "Subscription is already cancelled and cannot be reactivated"
        )

    if not subscription.stripe_subscription_id:
        raise HttpError(400, "No Stripe subscription found")

    try:
        stripe.Subscription.modify(
            subscription.stripe_subscription_id, cancel_at_period_end=False
        )

        subscription.cancel_at_period_end = False
        subscription.save()

        return {
            "message": "Subscription reactivated successfully",
            "next_billing_date": subscription.current_period_end.isoformat()
            if subscription.current_period_end
            else None,
        }

    except stripe.error.StripeError as e:
        raise HttpError(500, "Failed to reactivate subscription")
