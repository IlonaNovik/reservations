from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:reservation_id>", views.reservation, name="reservation")
]