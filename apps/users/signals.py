from django.db.models.signals import post_save
from django.dispatch import receiver
from utils.email_utils import send_verification_email 
from PhiBook.middleware import get_current_request
from .models import EmailVerificationToken
from .models import CustomUser, Profile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def send_verification_email_signal(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        request = get_current_request()
        ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        token = EmailVerificationToken.objects.create(
            user=instance,
            ip_address=ip,
            user_agent=user_agent
        )
        domain = "http://localhost:8000"
        verify_url = f"{domain}/api/verify/{token.token}/"
        send_verification_email(instance, verify_url)
