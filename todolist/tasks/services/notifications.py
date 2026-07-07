from todolist.tasks.selectors import get_tasks_stats, get_users_with_active_tasks
from todolist.todos.models import ReminderLog
from django.utils import timezone
from django.core.mail import send_mail
from todolist.todos.models import User



def send_daily_summary() -> None:
    users = get_users_with_active_tasks()
    for user in users:
        log, created = ReminderLog.objects.get_or_create(
            user=user,
            created_at=timezone.localdate(),
            defaults={"status": ReminderLog.Status.PENDING},
        )

        if not created and log.status != ReminderLog.Status.FAILED:
            continue

        try:
            if log.status == ReminderLog.Status.FAILED:
                log.status = ReminderLog.Status.PENDING
                log.save()
            
            
            
        except:
            pass

def send_reminder_email(user: User) -> None:
    body = {
        ""
    }