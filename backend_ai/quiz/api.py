from ninja import NinjaAPI
from .endpoints import router
from .auth import JWTAuth


api = NinjaAPI(title="e-TUTOR AI", version="1.0.0.", auth=JWTAuth())


api.add_router("/quiz", router)
