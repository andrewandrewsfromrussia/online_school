import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # замени "config" на имя твоего проекта

app = Celery("online_school")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
