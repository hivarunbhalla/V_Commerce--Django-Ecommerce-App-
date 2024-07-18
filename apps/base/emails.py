from django.conf import settings
from django.core.mail import send_mail

def send_account_activation_email(email_recipient, token):
    subject= 'Your account needs to be verified'
    email_form = settings.EMAIL_HOST_USER
    message = f'Hi, open below link in your browser to activate your account http://127.0.0.1:8000/accounts/activate/{token} '
    send_mail(subject, message, email_form, recipient_list=[email_recipient])