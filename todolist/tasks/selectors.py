from django.db.models.query import QuerySet
from todolist.tasks.models import Task
from django.contrib.auth.models import User
from todolist.api.v1.exceptions import TodoAppBaseError


def tasks_list(*, todo_id: int, user: User) -> QuerySet[Task]:

    return Task.objects.filter(todo_id=todo_id, todo__owner=user)


def get_task(task_id: int, user: User) -> Task:
    try:
        return Task.objects.get(id=task_id, todo__owner=user)
    except Task.DoesNotExist:
        raise TodoAppBaseError(
            message="Task not found.", extra={"task_id": task_id, "user_id": user.id}
        )
