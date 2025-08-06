from django.urls import path
from .views import UserProfileView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name= 'user-profile'),
    path("profile-update/", UserProfileView.as_view(), name='profile-update'),
]