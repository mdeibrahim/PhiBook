from django.urls import path
from .views import RegisterView, LoginView, LogoutView, VerifyAccountView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('verify/<int:pk>/', VerifyAccountView.as_view()),
]
