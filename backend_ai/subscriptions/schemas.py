from ninja import Schema
from ninja import ModelSchema
from subscriptions.models import SubscriptionPlan, Subscription
from core.utils import to_camel


class CheckoutRequest(Schema):
    plan_id: int
    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class CheckoutResponse(Schema):
    url: str
    session_id: str
    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class SubscriptionPlanSchema(ModelSchema):
    class Config:
        model = SubscriptionPlan
        model_fields = [
            "id",
            "name",
            "price",
            "description",
            "currency",
            "is_free",
        ]
        alias_generator = to_camel
        populate_by_name = True


class ListSubscriptionPlansSchema(Schema):
    actual_plan_id: int
    plans: list[SubscriptionPlanSchema]
    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class SubscriptionSchema(ModelSchema):
    class Config:
        model = Subscription
        model_fields = [
            "plan",
            "status",
            "current_period_start",
            "current_period_end",
            "cancel_at_period_end",
        ]
        alias_generator = to_camel
        populate_by_name = True
