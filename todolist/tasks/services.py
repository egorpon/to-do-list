from todolist.tasks.models import Task
from datetime import datetime
from django.db import transaction


@transaction.atomic
def task_create(
    *, name: str, description: str = "", due_date: datetime = None, todo_id: int
) -> Task:
    obj = Task(name=name, description=description, due_date=due_date, todo_id=todo_id)

    obj.full_clean()
    obj.save()

    return obj


@transaction.atomic
def task_update(*, data: dict, task: Task) -> Task:
    for field, value in data.items():
        setattr(task, field, value)

    task.full_clean()
    task.save()

    return task
