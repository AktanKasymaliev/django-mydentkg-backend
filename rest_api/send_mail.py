import os
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from .token import account_activation_token


def send_confirmation_email(request, user):
    current_site = get_current_site(request).domain
    context = {
        "small_text_detail": "Thank you for "
        "creating an account. "
        "Please verify your email "
        "address to set up your account.",
        "email": user.email,
        "domain": current_site,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": account_activation_token.make_token(user)
    }
    mail_subject = 'Active your account'
    to_email = user.email
    message = render_to_string('account/email.html', context)
    email = EmailMultiAlternatives(
        mail_subject,
        message,
        from_email=os.environ.get('EMAIL_HOST_USER'),
        to = [to_email],
    )
    email.content_subtype = 'html'
    email.send(fail_silently=True)