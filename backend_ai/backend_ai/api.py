from ninja import NinjaAPI
from quiz.api import router as quiz_router
from payments.api import router as payments_router
from authentication.api import router as auth_router
from authentication.auth import JWTAuth


api = NinjaAPI(title="e-TUTOR AI", version="1.0.0.", auth=JWTAuth())


api.add_router("/quiz", quiz_router, tags=["Quiz"])
api.add_router("/authentication", auth_router, tags=["Authentication"])
api.add_router("/payments", payments_router, tags=["Payments"], auth=None)
