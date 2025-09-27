from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("message/send/<str:secret_link>/",
         views.send_message, name="send_message"),
    path("messages/", views.get_messages, name="messages"),
    path("message/delete/<int:id>/", views.delete_message, name="delete_message"),
    path("users/", views.get_users, name="users"),
]
