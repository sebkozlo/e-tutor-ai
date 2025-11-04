from ninja import Router
from ninja.decorators import decorate_view
import stripe
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from payments.services.stripe_service import StripeService

router = Router()


@router.post("/webhook/stripe/", tags=["Stripe-Webhook"], auth=None)
@decorate_view(csrf_exempt)
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return HttpResponse(status=400)

    event_type = event.get("type")
    data_object = event.get("data", {}).get("object", {})

    if event_type == "checkout.session.completed":
        StripeService.handle_checkout_completed(data_object)

    if event_type == "invoice.payment_succeeded":
        StripeService.handle_payment_succeeded(data_object)

    if event_type == "customer.subscription.updated":
        StripeService.handle_subscription_updated(data_object)

    if event_type == "customer.subscription.deleted":
        StripeService.handle_subscription_cancelled(data_object)

    if event_type == "invoice.payment_failed":
        StripeService.handle_payment_failed(data_object)

    return HttpResponse(status=200)
