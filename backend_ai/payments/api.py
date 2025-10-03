from ninja import Router
import stripe
from ninja.errors import HttpError
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

router = Router()


@router.post("/webhook/stripe/", tags=["Stripe-Webhook"], auth=None)
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )

    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        stripe_response = event["data"]["object"]
        print(stripe_response)

    return HttpResponse(status=200)
