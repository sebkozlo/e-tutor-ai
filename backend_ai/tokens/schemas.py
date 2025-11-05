from ninja import Schema
from typing import Optional
from core.utils import to_camel


class PeriodUsage(Schema):
    usage: int
    limit: Optional[int]
    limit_exceeded: bool

    model_config = {"alias_generator": to_camel, "populate_by_name": True}


class TokenUsageResponse(Schema):
    day: PeriodUsage
    week: PeriodUsage
    month: PeriodUsage

    model_config = {"alias_generator": to_camel, "populate_by_name": True}