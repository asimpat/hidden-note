from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("message/send/<str:secret_link>/",
         views.SendMessageView.as_view(), name="send_message"),
    path("messages/", views.MessageListView.as_view(), name="messages"),
    path("message/<int:id>/", views.GetUpdateDeleteMessageView.as_view(),
         name="get_delete_message"),
    path("users/", views.UserListView.as_view(), name="users"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard")
]
