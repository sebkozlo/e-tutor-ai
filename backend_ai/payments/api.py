from ninja import Router
import stripe
from django.http import HttpResponse
from django.conf import settings
from payments.services.stripe_service import StripeService

router = Router()


@router.post("/webhook/stripe/", tags=["Stripe-Webhook"], auth=None)
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

    return HttpResponse(status=200)
