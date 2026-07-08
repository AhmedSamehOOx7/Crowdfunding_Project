from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .api_views import (
    UserRegistrationAPIView,
    UserLoginAPIView,
    UserProfileAPIView
)

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='api-register'),
    path('login/', UserLoginAPIView.as_view(), name='api-login'),
    path('refresh/', TokenRefreshView.as_view(), name='api-token-refresh'),
    path('profile/', UserProfileAPIView.as_view(), name='api-profile'),
]
