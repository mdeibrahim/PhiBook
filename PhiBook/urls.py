from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from .views import RootApiView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RootApiView.as_view(), name='root-api'),
    path('api/v1/', include('apps.authentication.urls')),
    path('api/v1/', include('apps.users.urls')),
    path('api/v1/', include('apps.dashboard.urls')),


    # for swagger documentation
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
