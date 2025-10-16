from core.models import ExternalUser
from customers.models import Customer
from subscriptions.models import Subscription, SubscriptionPlan
from ninja.errors import HttpError


def get_or_create_external_user(user_id: str, email: str) -> ExternalUser:
    external_user, created = ExternalUser.objects.get_or_create(
        external_id=user_id, defaults={"email": email}
    )
    return external_user, created


def setup_free_customer_and_subscription(external_user: ExternalUser, email: str):
    Customer.objects.get_or_create(
        external_user=external_user, defaults={"email": email}
    )

    free_plan = SubscriptionPlan.objects.filter(name="Free", is_free=True).first()
    if free_plan:
        Subscription.objects.get_or_create(
            external_user=external_user,
            defaults={"plan": free_plan, "status": "active"},
        )


def get_external_user_from_request(request):
    if not hasattr(request, "auth") or not request.auth:
        raise HttpError(401, "Unauthorized")

    user_id = request.auth.get("userId")
    email = request.auth.get("sub")

    if not user_id or not email:
        raise HttpError(401, "Invalid token payload")

    external_user, created = get_or_create_external_user(user_id, email)
    if created:
        setup_free_customer_and_subscription(external_user, email)

    return external_user


def get_existing_external_user(request) -> ExternalUser:
    if not hasattr(request, "auth") or not request.auth:
        raise HttpError(401, "Authentication required")

    user_id = request.auth.get("userId")
    if not user_id:
        raise HttpError(401, "Invalid token payload")

    try:
        external_user = ExternalUser.objects.get(external_id=user_id)
    except ExternalUser.DoesNotExist:
        raise HttpError(401, "Unauthorized")

    return external_user