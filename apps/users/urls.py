from django.urls import path
from .views import ViewUserProfileView, UpdateProfileView

urlpatterns = [
    path('view-profile/', ViewUserProfileView.as_view(), name= 'user-profile'),
    path("update-profile/", UpdateProfileView.as_view(), name='profile-update'),
]