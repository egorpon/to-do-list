from todolist.tasks.models import Task
from datetime import datetime
from django.db import transaction
from typing import Any
from django.utils import timezone


@transaction.atomic
def task_create(
    *,
    name: str,
    due_date: datetime = None,
    todo_id: int,
    description: str = "",
) -> Task:
    obj = Task(name=name, description=description, due_date=due_date, todo_id=todo_id)

    obj.full_clean()
    obj.save()

    return obj


def _apply_complete(*, task: Task, is_completed: bool) -> None:
    if is_completed and not task.is_completed:
        task.completed_at = timezone.now()
    elif not is_completed and task.is_completed:
        task.completed_at = None
    task.is_completed = is_completed


@transaction.atomic
def task_update(*, data: dict[str, Any], task: Task) -> Task:
    if "is_completed" in data:
        _apply_complete(task=task, is_completed=data.pop("is_completed"))
        
    for field, value in data.items():
        setattr(task, field, value)

    task.full_clean()
    task.save()

    return task


@transaction.atomic
def task_complete(*, task: Task) -> Task:
    task.is_completed = True
    task.completed_at = timezone.now()
    task.save(update_fields=["is_completed", "completed_at"])
    return task
