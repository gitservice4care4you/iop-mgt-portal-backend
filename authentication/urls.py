from django.urls import path
from .views import CustomTokenObtainPairView, CustomLoginWithAzureView
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path("login-with-email/", CustomTokenObtainPairView.as_view(), name="login"),
    path("login-with-azure/", CustomLoginWithAzureView.as_view(), name="login-azure"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
]


