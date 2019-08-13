from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from demo_project.settings import EMAIL_HOST_USER


@shared_task
def send_welcoming_email(username, email):
    send_mail(f'Hello {username}',
              'Thank you for registering',
              EMAIL_HOST_USER,
              [f'{email}'],
              )
