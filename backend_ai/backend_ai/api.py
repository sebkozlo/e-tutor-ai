from ninja import NinjaAPI
from quiz.api import router as quiz_router
from auth.api import router as auth_router
from auth.auth import JWTAuth


api = NinjaAPI(title="e-TUTOR AI", version="1.0.0.", auth=JWTAuth())


api.add_router("/quiz", quiz_router, tags=["Quiz"])
api.add_router("/auth", auth_router, tags=["Auth"])
