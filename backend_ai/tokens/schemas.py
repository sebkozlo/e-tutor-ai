from ninja import Schema


class TokenUsageCheckResponse(Schema):
    usage: int
    limit: int | None
    limit_exceeded: bool
