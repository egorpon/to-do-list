from todolist.tasks.services.notifications import send_daily_summary
from celery import shared_task
from smtplib import SMTPException


@shared_task(bind=True, max_retries=3)
def send_daily_summary_task(self):
    try:
        send_daily_summary()
    except SMTPException as exc:
        raise self.retry(exc=exc, countdown=30)
