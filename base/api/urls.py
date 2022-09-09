from django.urls import path
from . import views


urlpatterns = [
    path("", views.getRoutes),
    path("rooms/", views.getRooms, name="get-rooms"),
    path("rooms/<int:pk>/", views.getParticularRoom, name="get-particular-room"),
]