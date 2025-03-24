from ninja import NinjaAPI
from .endpoints import router


api = NinjaAPI(title='e-TUTOR AI', version='1.0.0.', )


api.add_router("/quiz", router)

