from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    TokenObtainPairResponseSerializer,
    TokenRefreshResponseSerializer,
    TokenVerifyResponseSerializer,
)
from .services.user_services import UserRegisterService, UserLoginService


class UserRegistrationView(APIView):
    """
    UserRegistrationView class for register new user
    """

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)
    service = UserRegisterService

    @swagger_auto_schema(responses={status.HTTP_200_OK: "ok"})
    def post(self, request) -> Response:
        return self.service(self).create_user(request)


class UserLoginView(APIView):
    """
    UserLoginView class for login user
    """

    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)
    service = UserLoginService

    @swagger_auto_schema(responses={status.HTTP_200_OK: "ok"})
    def post(self, request) -> Response:
        return self.service(self).user_login(request)


class DecoratedTokenObtainPairView(TokenObtainPairView):
    """
    class DecoratedTokenObtainPairView for realize token create
    and get opportunity for view this endpoint into documentation
    """

    @swagger_auto_schema(responses={status.HTTP_200_OK: TokenObtainPairResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    """
    class DecoratedTokenRefreshView for realize token refresh
    and get opportunity for view this endpoint into documentation
    """

    @swagger_auto_schema(responses={status.HTTP_200_OK: TokenRefreshResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenVerifyView(TokenVerifyView):
    """
    class DecoratedTokenVerifyView for realize token verify
    and get opportunity for view this endpoint into documentation
    """

    @swagger_auto_schema(responses={status.HTTP_200_OK: TokenVerifyResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
