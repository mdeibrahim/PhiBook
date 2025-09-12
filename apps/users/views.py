from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Profile
from .serializers import ProfileSerializer


class ViewUserProfileView(APIView):
    """
    User profile management (GET).
    
    **Authentication:** Required
    **GET:** Retrieve profile data
    **Response:** Profile data or errors
    """
    permission_classes = [IsAuthenticated]  
    
    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile, context={'request': request})
            return Response({
                "status": "success",
                "status_code": 200,
                "message": "Profile retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(
                {
                    "status": "error",
                    "status_code": 404,
                    "message": "Profile not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
    
    def put(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "status_code": 200,
                    "message": "Profile updated successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                "status": "error",
                "status_code": 400,
                "message": "Invalid data provided",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({
                "status": "error",
                "status_code": 404,
                "message": "Profile not found"
            }, status=status.HTTP_404_NOT_FOUND)


class UpdateProfileView(APIView):
    """
    Update profile (full_name, date_of_birth, bio, profile_picture)

    **Authentication:** Required
    **Request Body:** full_name, date_of_birth, bio, profile_picture
    **Response:** Profile data or errors
    """
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "status_code": 200,
                    "message": "Profile updated successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                "status": "error",
                "status_code": 400,
                "message": "Invalid data provided",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({
                "status": "error",
                "status_code": 404,
                "message": "Profile not found"
            }, status=status.HTTP_404_NOT_FOUND)
