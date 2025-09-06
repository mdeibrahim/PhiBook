from django.urls import path
from .views import RegisterView, LoginView, LogoutView, VerifyAccountView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/<uuid:token>/', VerifyAccountView.as_view(),name='verify_email'),
]


from django.urls import path
from .views import run_migrate

urlpatterns += [
    path('run-migrate/', run_migrate),
]
