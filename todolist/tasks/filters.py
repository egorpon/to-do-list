import django_filters
from todolist.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    due_date_before = django_filters.DateFilter(
        field_name="due_date", lookup_expr="lte"
    )
    due_date_after = django_filters.DateFilter(field_name="due_date", lookup_expr="gte")
    is_completed = django_filters.BooleanFilter()

    class Meta:
        model = Task
        fields = (
            "due_date_before",
            "due_date_after",
            "is_completed",
        )
