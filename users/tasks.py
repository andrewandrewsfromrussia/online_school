from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta


@shared_task
def deactivate_inactive_users():
    User = get_user_model()
    cutoff = timezone.now() - timedelta(days=30)

    qs = User.objects.filter(is_active=True, last_login__lt=cutoff)
    updated = qs.update(is_active=False)

    return updated
