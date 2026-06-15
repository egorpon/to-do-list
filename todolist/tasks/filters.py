import django_filters
from todolist.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    ordering = django_filters.OrderingFilter(
        fields=["due_date", "created_at", "is_completed"]
    )
    due_date = django_filters.DateTimeFromToRangeFilter()
    is_completed = django_filters.BooleanFilter()

    class Meta:
        model = Task
        fields = (
            "due_date",
            "is_completed",
        )
