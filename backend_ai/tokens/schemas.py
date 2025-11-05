from ninja import Schema
from core.utils import to_camel


class TokenUsageCheckResponse(Schema):
    usage: int
    limit: int | None
    limit_exceeded: bool
    subscription_plan: str | None = None
    model_config = {"alias_generator": to_camel, "populate_by_name": True}
