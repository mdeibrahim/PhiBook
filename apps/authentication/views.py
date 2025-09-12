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
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from django.shortcuts import redirect
from django.conf import settings

class RegisterView(APIView):
    """
    User registration with email verification.
    
    **Request Body:** email, password, password_confirm
    **Response:** User data or validation errors
    """
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=RegisterSerializer,
    )
    
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
            "message": "Registration failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# class VerifyAccountView(APIView):
#     """
#     Email verification using token.
    
#     **URL Parameters:** token (UUID)
#     **Response:** Success message or error details
#     """
#     permission_classes = [permissions.AllowAny]
    
#     def get(self, request, token):
#         user_agent = request.META.get('HTTP_USER_AGENT', '')
#         ip_address = request.META.get('REMOTE_ADDR')

#         token_object = get_object_or_404(EmailVerificationToken, token=token, is_used=False)


#         if token_object.created_at + timedelta(minutes=15) < now():
#             return Response({
#                 "status": "error",
#                 "status_code": status.HTTP_400_BAD_REQUEST,
#                 "message": "Verification token has expired."
#             }, status=status.HTTP_400_BAD_REQUEST)

#         # if token_object.ip_address != ip_address or token_object.user_agent != user_agent:
        
#         if token_object.ip_address != ip_address:
#             return Response({
#                 "status": "error",
#                 "status_code": status.HTTP_403_FORBIDDEN,
#                 "message": "This device is not allowed to verify this account."
#             }, status=status.HTTP_403_FORBIDDEN)

#         token_object.user.is_active=True
#         token_object.user.save()
#         token_object.is_used=True
#         token_object.save()

#         return Response({
#             "status": "success",
#             "status_code": status.HTTP_200_OK,
#             "message": "Account verified successfully. You can now login."
#         }, status=status.HTTP_200_OK)
class VerifyAccountView(APIView):
    """
    Email verification using token with redirect to frontend.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        ip_address = request.META.get('REMOTE_ADDR')

        token_object = get_object_or_404(EmailVerificationToken, token=token, is_used=False)

        # check expiry
        if token_object.created_at + timedelta(minutes=15) < now():
            redirect_url = f"{settings.FRONTEND_URL}/verify-result?status=error&message=Verification token has expired."
            return redirect(redirect_url)

        # check ip / device
        # if token_object.ip_address != ip_address:
        #     redirect_url = f"{settings.FRONTEND_URL}/verify-result?status=error&message=This device is not allowed to verify this account."
        #     return redirect(redirect_url)

        # activate user
        token_object.user.is_active = True
        token_object.user.save()
        token_object.is_used = True
        token_object.save()

        # success redirect
        redirect_url = f"{settings.FRONTEND_URL}/verify-result?status=success&message=Account verified successfully. You can now login."
        return redirect(redirect_url)

class LoginView(APIView):
    """
    User authentication with token return.
    
    **Request Body:** email, password
    **Response:** Authentication token or validation errors
    """
    permission_classes = [permissions.AllowAny]
    
    @extend_schema(
        request=LoginSerializer
    )

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "status": "success",
                "status_code": status.HTTP_200_OK,
                "message": "Login successful",
                "data": {
                    "token": token.key
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": "Login failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    """
    Invalidate authentication token.
    
    **Authentication:** Required
    **Response:** Success message
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "message": "Logged out successfully."
        }, status=status.HTTP_200_OK)
