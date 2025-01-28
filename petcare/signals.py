from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings

def send_email_confirmation(user, request):
    """
    Sends an email confirmation to the given user with a verification link.
    """
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk)) 
    confirm_url = request.build_absolute_uri(reverse('confirm_email', args=[uid, token]))

    subject = 'Confirm Your Email Address'
    message = render_to_string('emails/confirm_email.html', {'confirm_url': confirm_url, 'user': user})

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  
        [user.email],  
        fail_silently=False
    )
