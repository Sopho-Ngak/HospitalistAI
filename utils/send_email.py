from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_verification_code(username,email, code):
    try:
        context = {
            'verify_code': code,
            'name': username,
            'reset_password': True
        }
        html_content = render_to_string('verification_code_email_template.html', context)
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            'Verification Code',
            text_content,
            settings.EMAIL_HOST_USER,
            [email],
        )
        email.attach_alternative(html_content, 'text/html')
        email.send()
    except Exception as e:
        with open('error.txt', 'w') as f:
            f.write(str(e))