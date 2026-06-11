from todolist.todos.models import TodoList
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q


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
    )


def todos_list(*, owner=None) -> QuerySet[TodoList]:

    return _todos_queryset().filter(owner=owner)
    


def get_todo(todo_id, owner) -> TodoList:

    todo = get_object_or_404(_todos_queryset(), id=todo_id, owner=owner)

    return todo
