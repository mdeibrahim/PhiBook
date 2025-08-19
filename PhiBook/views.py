from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.urls import reverse


class RootApiView(APIView):
    """
    Root API endpoint that provides information about the API and available endpoints.
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """
        GET request to root endpoint returns API information and available endpoints.
        """
        base_url = request.build_absolute_uri('/')[:-1] 
        
        api_endpoints = {
            "authentication": {
                "description": "User authentication endpoints",
                "url": f"{base_url}/api/v1/",
                "endpoints": [
                    "register",
                    "login", 
                    "logout",
                    "verify/<uuid:token>"
                ]
            },
            "users": {
                "description": "User management endpoints",
                "url": f"{base_url}/api/v1/",
                "endpoints": [
                    "profile",
                    "profile-update"
                ]
            },
            "dashboard": {
                "description": "Social media dashboard endpoints",
                "url": f"{base_url}/api/v1/",
                "endpoints": [
                    "create-post",
                    "update-post/<int:pk>",
                    "delete-post/<int:pk>",
                    "view-my-posts",
                    "view-all-posts",
                    "posts/<int:pk>/like-unlike",
                    "add-comment/<int:pk>",
                    "update-comment/<int:pk>",
                    "delete-comment/<int:pk>",
                    "view-all-comments/<int:pk>"
                ]
            },
            "documentation": {
                "description": "API documentation",
                "endpoints": [
                    f"{base_url}/api/v1/docs/",
                    f"{base_url}/api/v1/redoc/"
                ]
            }
        }
        
        response_data = {
            "status": "success",
            "status_code": 200,
            "message": "Welcome to PhiBook API",
            "api_info": {
                "name": "PhiBook API",
                "version": "1.0.0",
                "description": "A social media platform API built with Django REST Framework",
                "base_url": f"{base_url}/api/v1/",
                "documentation": f"{base_url}/api/v1/docs/"
            },
            "available_endpoints": api_endpoints,
            "usage": {
                "authentication": "Most endpoints require authentication. Use the authentication endpoints to get access tokens.",
                "rate_limiting": "API requests are rate-limited to ensure fair usage.",
                "response_format": "All responses follow a consistent format with status, message, and data fields."
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        POST request to root endpoint returns the same information as GET.
        """
        return self.get(request)
    
    def options(self, request):
        """
        OPTIONS request for CORS preflight.
        """
        response = Response(status=status.HTTP_200_OK)
        response["Allow"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response
