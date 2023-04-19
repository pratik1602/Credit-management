from django.core.mail import send_mail
import random
from django.conf import settings
from usercredit.models import *
from celery import shared_task
from time import sleep


@shared_task
def sleepy(duration):
    sleep(duration)
    return None


@shared_task
def send_otp_via_email(email):
    subject = 'Your account verification email '
    otp = random.randint(1000, 9999)
    message = f'Your otp is {otp}'
    email_from =  settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email], fail_silently= False)
    user_obj = User.objects.get(email = email)
    user_obj.otp = otp
    user_obj.save()
    return None