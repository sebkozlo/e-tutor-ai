from ninja import Router
from ninja.errors import HttpError
from .models import TokenUsage
from users.models import ExternalUser
from .schemas import TokenUsageResponse, PeriodUsage
from core.enums import PeriodicChoices


router = Router()


@router.get("/usage", response=TokenUsageResponse, by_alias=True)
def get_token_usage(request):
    external_uuid = request.auth.get("userId")
    if not external_uuid:
        raise HttpError(401, "Authentication required.")

    try:
        user = ExternalUser.objects.get(external_id=external_uuid)
    except ExternalUser.DoesNotExist:
        raise HttpError(404, "User not found.")

    day_usage, day_limit, day_exceeded = TokenUsage.check_limit(user, PeriodicChoices.DAY)
    week_usage, week_limit, week_exceeded = TokenUsage.check_limit(user, PeriodicChoices.WEEK)
    month_usage, month_limit, month_exceeded = TokenUsage.check_limit(user, PeriodicChoices.MONTH)

    return {
        "day": {
            "usage": day_usage,
            "limit": day_limit,
            "limit_exceeded": day_exceeded,
        },
        "week": {
            "usage": week_usage,
            "limit": week_limit,
            "limit_exceeded": week_exceeded,
        },
        "month": {
            "usage": month_usage,
            "limit": month_limit,
            "limit_exceeded": month_exceeded,
        }
    }