from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Profile
from .serializers import ProfileSerializer


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  
    
    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response({
                "Status": "true",
                "status_code": 200,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(
                {
                    "Status": "false",
                    "status_code": 404,
                    "error": "Profile not found"
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
                    "Status": "true",
                    "status_code": 200,
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                "Status": "false",
                "status_code": 400,
                "error": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({
                "Status": "false",
                "status_code": 404,
                "error": "Profile not found"
            }, status=status.HTTP_404_NOT_FOUND)
