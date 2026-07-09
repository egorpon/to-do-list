from celery import Celery
import os
from config.env import env

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    env.str("DJANGO_SETTINGS_MODULE", default="config.django.local"),
)

app = Celery("todolist")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

