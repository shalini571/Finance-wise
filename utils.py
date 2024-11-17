# authentication/utils.py
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_password_reset_email(user, reset_url):
    """Send password reset email to user"""
    context = {
        'user': user,
        'reset_url': reset_url,
        'site_name': 'Your Site Name'
    }
    
    # Render email templates
    html_content = render_to_string('authentication/email/password_reset_email.html', context)
    text_content = strip_tags(html_content)
    
    # Create email
    subject = 'Password Reset Request'
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

def send_account_activation_email(user, activation_url):
    """Send account activation email to user"""
    context = {
        'user': user,
        'activation_url': activation_url,
        'site_name': 'Your Site Name'
    }
    
    # Render email templates
    html_content = render_to_string('authentication/email/activation_email.html', context)
    text_content = strip_tags(html_content)
    
    # Create email
    subject = 'Activate Your Account'
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()