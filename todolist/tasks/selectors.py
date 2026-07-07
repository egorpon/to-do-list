from django.db.models.query import QuerySet
from todolist.tasks.models import Task
from django.contrib.auth.models import User
from todolist.api.v1.exceptions import TodoAppBaseError
from django.utils import timezone
import datetime
from django.db.models import Count, Q


def tasks_list(*, todo_id: int, user: User) -> QuerySet[Task]:

    return Task.objects.filter(todo_id=todo_id, todo__owner=user).order_by(
        "-created_at"
    )


def get_task(task_id: int) -> Task:
    try:
        return Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise TodoAppBaseError(message="Task not found.", extra={"task_id": task_id})


def get_tasks_stats(*, user: User) -> dict:
    today = timezone.now()

    return Task.objects.filter(todo__owner=user).aggregate(
        overdue_count=Count("id", filter=Q(due_date__lt=today, is_completed=False)),
        upcoming_count=Count("id", filter=Q(due_date__gte=today, is_completed=False)),
        completed_count=Count("id", filter=Q(is_completed=True)),
        total_count=Count("id"),
    )


def get_overdue_tasks(*, user: User) -> QuerySet[Task]:
    today = timezone.now()

    return Task.objects.filter(todo__owner=user, due_date__lt=today, is_completed=False)


def get_upcoming_tasks_this_week(*, user: User) -> QuerySet[Task]:
    today = timezone.now()
    week_start = today - datetime.timedelta(days=today.weekday())
    week_end = week_start + datetime.timezone(days=6)

    return Task.objects.filter(
        todo__owner=user,
        due_date__gte=week_start,
        due_date__lte=week_end,
        is_completed=False,
    )


def get_users_with_active_tasks() -> QuerySet[User]:
    return User.objects.filter(todolists__tasks__is_completed=False).distinct()
