from rest_framework import status
from rest_framework.response import Response


class BaseUserService:
    def __init__(self, context):
        self.context = context


class UserRegisterService(BaseUserService):
    def create_user(self, request) -> Response:
        serializer = self.context.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                "success": True,
                "statusCode": status_code,
                "message": "User successfully registered!",
                "user": serializer.data,
            }

            return Response(response, status=status_code)


class UserLoginService(BaseUserService):
    def user_login(self, request) -> Response:
        serializer = self.context.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            status_code = status.HTTP_200_OK

            response = {
                "success": True,
                "statusCode": status_code,
                "message": "User logged in successfully",
                "access": serializer.data["access"],
                "refresh": serializer.data["refresh"],
                "authenticatedUser": {
                    "email": serializer.data["email"],
                },
            }

            return Response(response, status=status_code)
