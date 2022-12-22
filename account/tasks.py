from celery import shared_task
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status


@shared_task
def send_email_task(username, token, reciever_email):

    body = f"Hi {username},\n You are seeing this message because you registered for Ebookify . Copy the code code below to verify your account   \n {token}"

    send_mail(
        "Confirmation code for account verification",
        body,
        "anova96developer@gmail.com",
        [reciever_email],
        fail_silently=False,
    )
    return None
