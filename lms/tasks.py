from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail



@shared_task
def ping():
    return "pong"

@shared_task
def send_course_update_email(recipient_email: str, course_title: str, course_id: int):
    send_mail(
        subject=f"Обновление курса: {course_title}",
        message=(
            f"Курс «{course_title}» был обновлён.\n"
            f"ID курса: {course_id}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_email],
        fail_silently=False,
    )
