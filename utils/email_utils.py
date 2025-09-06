from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags


def send_verification_email(user, verification_link):
    """
    Send account verification email to user
    """
    subject = 'Verify Your PhiBook Account'
    
    # HTML version of the email
    html_message = f"""
    <html>
        <body>
            <h2>Welcome to PhiBook!</h2>
            <p>Hi {user.email.split('@')[0]},</p>
            <p>Thank you for registering with PhiBook. Please click the link below to verify your account:</p>
            <p><a href="{verification_link}">Verify Account</a></p>
            
            <p>This link will expire in 24 hours.</p>
            <p>Best regards,<br>The PhiBook Team</p>
        </body>
    </html>
    """
    
    # Plain text version
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_password_reset_email(user, reset_url):
    """
    Send password reset email to user
    """
    subject = 'Reset Your PhiBook Password'
    
    html_message = f"""
    <html>
        <body>
            <h2>Password Reset Request</h2>
            <p>Hi {user.email.split('@')[0]},</p>
            <p>You requested a password reset for your PhiBook account. Click the link below to reset your password:</p>
            <p><a href="{reset_url}">Reset Password</a></p>
            <p>If you didn't request this, please ignore this email.</p>
            <p>This link will expire in 1 hour.</p>
            <p>Best regards,<br>The PhiBook Team</p>
        </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_welcome_email(user):
    """
    Send welcome email to newly registered user
    """
    subject = 'Welcome to PhiBook!'
    
    html_message = f"""
    <html>
        <body>
            <h2>Welcome to PhiBook!</h2>
            <p>Hi {user.email.split('@')[0]},</p>
            <p>Thank you for joining PhiBook! Your account has been successfully created.</p>
            <p>You can now log in and start using our platform.</p>
            <p>Best regards,<br>The PhiBook Team</p>
        </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False 