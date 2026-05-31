from .serializers import TaskSerializer
from rest_framework import generics, filters
from todolist.tasks.models import Task
from todolist.tasks.filters import TaskFilter
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.


class TaskListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["name"]
    ordering_fields = ["due_date", "created_at", "is_completed"]

    queryset = Task.objects.none()

    def get_queryset(self):
        todo_list_id = self.kwargs["list_id"]
        return Task.objects.filter(todo__owner=self.request.user, todo=todo_list_id)
