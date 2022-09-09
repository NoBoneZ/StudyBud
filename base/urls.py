from django.urls import path
from . import views


app_name = "base"

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("", views.home, name="home"),
    path("profile/<int:pk>/", views.userprofile, name="profile"),
    path("profile/<int:pk>/update_user", views.updateuser, name="update-user"),
    path("room/<int:pk>/", views.room, name="room"),
    path("room/<int:pk>/delete_message/<int:id>/", views.delete_message, name='delete-message'),
    path("create-room/", views.createroom, name="create-room"),
    path("update_room/<int:pk>", views.updateRoom, name="update-room"),
    path("delete-room/<int:pk>", views.deleteRoom, name="delete-room"),
    path("topics/", views.topicspage, name="topics"),
    path("activity/", views.activitypage, name="activity")
    
]