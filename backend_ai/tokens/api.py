from ninja import Router
from ninja.errors import HttpError
from .models import TokenUsage
from core.models import ExternalUser
from .schemas import TokenUsageCheckResponse
from core.enums import PeriodicChoices


router = Router()


@router.get("/usage", response=TokenUsageCheckResponse)
def get_token_usage(request, period: str = "day"):
    external_uuid = request.auth.get("userId")
    if not external_uuid:
        raise HttpError(401, "Authentication required.")

    try:
        user = ExternalUser.objects.get(external_id=external_uuid)
    except ExternalUser.DoesNotExist:
        raise HttpError(404, "User not found.")

    period = period.lower()

    # Walidacja okresu
    period_map = {
        "day": PeriodicChoices.DAY,
        "week": PeriodicChoices.WEEK,
        "month": PeriodicChoices.MONTH,
    }

    if period not in period_map:
        raise HttpError(400, f"Invalid period. Choose: {', '.join(period_map.keys())}")

    period_choice = period_map[period]
    usage, limit, exceeded = TokenUsage.check_limit(user, period_choice)

    return TokenUsageCheckResponse(usage=usage, limit=limit, limit_exceeded=exceeded)
