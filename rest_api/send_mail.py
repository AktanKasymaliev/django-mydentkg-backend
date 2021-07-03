import os
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from .token import account_activation_token
from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

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
    send_mail(
        mail_subject,
        message,
        EMAIL_HOST_USER,
        [to_email, ],
        html_message=message,
    )