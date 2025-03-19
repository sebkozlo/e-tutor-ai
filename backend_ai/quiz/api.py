from ninja import NinjaAPI
from .enpoints import router

api = NinjaAPI(title='e-TUTOR AI')
api.add_router("/quiz", router)

from django.urls import path

urlpatterns = [
    path("api/", api.urls),
]