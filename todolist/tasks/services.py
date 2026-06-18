from todolist.tasks.models import Task
from datetime import datetime
from django.db import transaction
from typing import Any


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


@transaction.atomic
def task_update(*, data: dict[str, Any], task: Task) -> Task:
    for field, value in data.items():
        setattr(task, field, value)

    task.full_clean()
    task.save()

    return task
