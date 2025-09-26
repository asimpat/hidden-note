from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import register, send_message, get_messages, delete_message

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("message/send/<str:secret_link>/", send_message, name="send_message"),
    path("messages/", get_messages, name="messages"),
    path("message/delete/<int:id>/", delete_message, name="delete_message"),
]
 