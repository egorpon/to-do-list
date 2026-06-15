from django.db.models.query import QuerySet
from todolist.tasks.models import Task
from todolist.tasks.filters import TaskFilter
from django.shortcuts import get_object_or_404


def tasks_list(*, filters=None, todo_id, user) -> QuerySet[Task]:

    filters = filters or {}
    qs = Task.objects.filter(todo=todo_id, todo__owner=user)
    return TaskFilter(filters, qs).qs


def get_task(task_id, user):
    task = get_object_or_404(Task, id=task_id, todo__owner=user)

    return task