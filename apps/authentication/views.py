from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from .serializers import RegisterSerializer, LoginSerializer
import uuid
from apps.users.models import EmailVerificationToken, CustomUser
from datetime import timedelta
from django.utils.timezone import now

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.token = uuid.uuid4().hex
            user.save()
            return Response({
                "status": "success",
                "status_code": status.HTTP_201_CREATED,
                "message": "User registered. Please check email to verify account.",
                "data": {
                    "id": user.id,
                    "is_active": user.is_active,
                    "email": user.email,
                    "token": user.token,
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "Registration failed.",
            "errors-message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class VerifyAccountView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, token):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        ip_address = request.META.get('REMOTE_ADDR')

        token_object = get_object_or_404(EmailVerificationToken, token=token, is_used=False)


        if token_object.created_at + timedelta(minutes=15) < now():
            return Response({
                "status": "error",
                "status_code": status.HTTP_400_BAD_REQUEST,
                "error-message": "Verification token has expired."
            }, status=status.HTTP_400_BAD_REQUEST)

        # if token_object.ip_address != ip_address or token_object.user_agent != user_agent:
        if token_object.ip_address != ip_address:
            return Response({
                "status": "error",
                "status_code": status.HTTP_403_FORBIDDEN,
                "error": "This device is not allowed to verify this account."
            }, status=status.HTTP_403_FORBIDDEN)

        token_object.user.is_active=True
        token_object.user.save()
        token_object.is_used=True
        token_object.save()

        return Response({
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "message": "Account verified successfully. You can now login."
        }, status=status.HTTP_200_OK)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "status": "success",
                "status_code": status.HTTP_200_OK,
                "token": token.key
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "status_code": status.HTTP_400_BAD_REQUEST,
            "errors-message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "message": "Logged out successfully."
        }, status=status.HTTP_200_OK)
