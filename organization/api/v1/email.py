from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from core.settings import EMAIL_HOST_USER

def send_welcome_email(user_email, user_name):
    html_content = render_to_string('email_templates/welcome_email.html', {
        'user_name': user_name
    })

    email = EmailMessage(
        subject='Welcome to E-Commerce!',
        body=html_content,
        from_email=EMAIL_HOST_USER,
        to=[user_email],
    )
    email.content_subtype = 'html'
    email.send()
