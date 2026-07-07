from todolist.todos.models import TodoList, User
from django.db import transaction
from typing import Any
from todolist.todos.models import ReminderLog
from django.utils import timezone
from django.core.mail import send_mail


@transaction.atomic
def todolist_create(*, name: str, owner: User, description: str = "") -> TodoList:

    obj = TodoList(name=name, description=description, owner=owner)

    obj.full_clean()
    obj.save()

    return obj


@transaction.atomic
def todolist_update(*, data: dict[str, Any], todo: TodoList) -> TodoList:

    for field, value in data.items():
        setattr(todo, field, value)

    todo.full_clean()
    todo.save()

    return todo


def send_planning_reminders() -> None:
        log, created = ReminderLog.objects.get_or_create(
            created_at=timezone.localdate(),
            defaults={"status": ReminderLog.Status.PENDING},
        )

        # if not created and log.status != ReminderLog.Status.FAILED:
        #     continue

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