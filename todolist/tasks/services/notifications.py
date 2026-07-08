from todolist.tasks.selectors import (
    get_tasks_stats,
    get_overdue_tasks,
    get_upcoming_tasks_this_week,
    get_completed_tasks_this_week,
    get_users_with_active_tasks,
)
from todolist.todos.models import ReminderLog
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from smtplib import SMTPException


def send_daily_summary() -> None:
    users = get_users_with_active_tasks()
    for user in users:
        log, created = ReminderLog.objects.get_or_create(
            user=user,
            date=timezone.localdate(),
            defaults={"status": ReminderLog.Status.PENDING},
        )

        if not created and log.status == ReminderLog.Status.SUCCESS:
            continue

        try:
            if log.status == ReminderLog.Status.FAILED:
                log.status = ReminderLog.Status.PENDING
                log.save()

            stats = get_tasks_stats(user=user)
            overdue_tasks = get_overdue_tasks(user=user)
            upcoming_tasks_this_week = get_upcoming_tasks_this_week(user=user)
            completed_tasks_this_week = get_completed_tasks_this_week(user=user)
            plain_message, html_message = build_summary_email(
                user=user,
                stats=stats,
                overdue_tasks=overdue_tasks,
                upcoming_tasks_this_week=upcoming_tasks_this_week,
                completed_tasks_this_week=completed_tasks_this_week,
            )

            send_mail(
                subject="Your daily summary",
                message=plain_message,
                html_message=html_message,
                from_email=None,
                recipient_list=[user.email],
            )

            log.status = ReminderLog.Status.SUCCESS
            log.save()

        except  SMTPException as exc:
            log.status = ReminderLog.Status.FAILED
            log.error_message = str(exc)
            log.save()
            has_error = True

    if has_error:
        raise SMTPException("SMTP server connection failed.")



def build_summary_email(
    *,
    user: User,
    stats: dict,
    overdue_tasks,
    upcoming_tasks_this_week,
    completed_tasks_this_week,
) -> tuple[str, str]:
    context = {
        "date": timezone.localdate(),
        "username": user.username,
        "overdue_tasks": overdue_tasks,
        "upcoming_tasks_this_week": upcoming_tasks_this_week,
        "completed_tasks_this_week": completed_tasks_this_week,
        **stats,
    }

    html_message = render_to_string(
        "tasks/emails/daily_summary_email.html",
        context=context,
    )
    plain_message = strip_tags(html_message)

    return plain_message, html_message
