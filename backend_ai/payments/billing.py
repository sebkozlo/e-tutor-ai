import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_customer(email: str, name: str) -> stripe.Customer:
    customer = stripe.Customer.create(email=email, name=name)
    return customer


def customer_list():
    return stripe.Customer.list()
