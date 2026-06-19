from django.db.models.query import QuerySet
from todolist.tasks.models import Task
from rest_framework.exceptions import NotFound
from django.contrib.auth.models import User
from todolist.api.v1.exceptions import TaskNotFound


def tasks_list(*, todo_id: int, user: User) -> QuerySet[Task]:

    return Task.objects.filter(todo_id=todo_id, todo__owner=user)


def get_task(task_id: int, user: User) -> Task:
    try:
        return Task.objects.get(id=task_id, todo__owner=user)
    except Task.DoesNotExist:
        raise TaskNotFound()
