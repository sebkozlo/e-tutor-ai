from ninja import NinjaAPI
from .enpoints import router

api = NinjaAPI(title='e-TUTOR AI', version='1.0.0')


api.add_router("/quiz", router)

from django.urls import path

urlpatterns = [
    path("api/", api.urls),
]