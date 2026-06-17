import django_filters
from todolist.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    due_date = django_filters.DateTimeFromToRangeFilter()
    is_completed = django_filters.BooleanFilter()

    class Meta:
        model = Task
        fields = ()
