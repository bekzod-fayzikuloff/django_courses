from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .serializers import UserRegistrationSerializer, UserLoginSerializer
from .services.user_services import UserRegisterService, UserLoginService


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)
    service = UserRegisterService

    def post(self, request) -> Response:
        return self.service(self).create_user(request)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)
    service = UserLoginService

    def post(self, request) -> Response:
        return self.service(self).user_login(request)
