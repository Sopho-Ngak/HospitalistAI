from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
import datetime

from accounts.models import User, VerificationCode
from utils.code_generator import generate_code


@receiver(post_save, sender=User)
def account_activation_code(sender, instance, created, **kwargs):
    if created:
        user_code = VerificationCode.objects.create(
            user=instance, code=generate_code())
        context = {
            'verify_code': user_code.code,
            'name': instance.username,
        }
        html_content = render_to_string(
            'verification_code_email_template.html', context)
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            'Verification Code',
            text_content,
            settings.EMAIL_HOST_USER,
            [instance.email],
        )
        email.attach_alternative(html_content, 'text/html')
        email.send()


@receiver(pre_save, sender=VerificationCode)
def delete_all_expired_code(sender, instance, **kwargs):
    VerificationCode.objects.filter(
        created_at__lt=timezone.now() - datetime.timedelta(minutes=25)).delete()
