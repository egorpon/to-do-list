from celery import shared_task


@shared_task(bind=True, max_retries=3)
def send_daily_summary_task(self):

    from todolist.tasks.services.notifications import send_daily_summary

    has_error = send_daily_summary()

    if has_error:
        self.retry(countdown=30)
