"""
    API auth path endpoints define module
"""
from django.urls import path

from .views import (
    UserRegistrationView,
    UserLoginView,
    DecoratedTokenObtainPairView,
    DecoratedTokenRefreshView,
    DecoratedTokenVerifyView,
)


urlpatterns = [
    path("token/obtain/", DecoratedTokenObtainPairView.as_view(), name="token_create"),
    path("token/refresh/", DecoratedTokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", DecoratedTokenVerifyView.as_view(), name="token_verify"),
    path("jwt_register/", UserRegistrationView.as_view(), name="register"),
    path("jwt_login/", UserLoginView.as_view(), name="login"),
]
