from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from utils.email_utils import send_verification_email 

from .models import CustomUser, Profile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def send_verification_email_signal(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        domain = "http://localhost:8000"
        verify_url = f"{domain}/api/verify/{instance.pk}/"
        send_verification_email(instance, verify_url)
