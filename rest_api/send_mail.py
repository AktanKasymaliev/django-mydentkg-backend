import os
from customUser.models import User
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from .token import account_activation_token
from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.utils.html import strip_tags

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
        "token": account_activation_token.make_token(user),
    }

    message = render_to_string('account/email.html', context) if isinstance(user, User) \
    else render_to_string("account/email_doctors.html", context)
    mail_subject = 'Active your account'
    to_email = user.email
    send_mail(
        mail_subject,
        message,
        EMAIL_HOST_USER,
        [to_email, ],
        html_message=message,
    )

def password_reset_token_created(request, *args, **kwargs):
    current_site = get_current_site(request).domain
    context = {
        "small_text_detail": "Сброс пароля",
        "for_pass_confirm": "Нажмите на кнопку что бы создать новый пароль",
        "email": request.user.email,
        "domain": current_site,
        "uid": urlsafe_base64_encode(force_bytes(request.user.pk)),
        "token": account_activation_token.make_token(request.user),
    }

    msg_html = render_to_string("account/reset_password_email.html", context)
    plain_message = strip_tags(msg_html)
    subject = "Reset password"

    send_mail(
        subject,
        plain_message,
        # from:
        EMAIL_HOST_USER,
        # to:
        [request.user.email],
        html_message=msg_html,
    )