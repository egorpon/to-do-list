from todolist.todos.models import TodoList
from django.db.models.query import QuerySet
from django.utils import timezone
from django.db.models import Count, Q
from todolist.api.v1.exceptions import TodoAppBaseError
from django.contrib.auth.models import User


def _todos_queryset():
    return TodoList.objects.annotate(
        tasks_count=Count("tasks"),
        tasks_done=Count("tasks", filter=Q(tasks__is_completed=True)),
        tasks_pending=Count("tasks", filter=Q(tasks__is_completed=False)),
        upcoming_tasks=Count(
            "tasks",
            filter=Q(tasks__is_completed=False, tasks__due_date__gt=timezone.now()),
        ),
        overdue_tasks=Count(
            "tasks",
            filter=Q(tasks__is_completed=False, tasks__due_date__lt=timezone.now()),
        ),
    ).order_by("-created_at")


def todos_list(*, owner=None) -> QuerySet[TodoList]:

    return _todos_queryset().filter(owner=owner)


def get_todo(todo_id: int, owner: User) -> TodoList:

    try:
        return _todos_queryset().get(id=todo_id, owner=owner)

    except TodoList.DoesNotExist:
        raise TodoAppBaseError(
            message="Todo list not found.", extra={"todo_id": todo_id, "user": owner.id}
        )
