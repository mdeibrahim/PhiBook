from django.urls import path

from apps.subscription.views import CreateSubscriptionView

urlpatterns = [
    path('create-subscription/', CreateSubscriptionView.as_view(), name='create-subscription'),
]