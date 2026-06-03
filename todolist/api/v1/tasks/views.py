from .serializers import TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer
from rest_framework import generics, filters
from todolist.tasks.models import Task
from todolist.tasks.filters import TaskFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from todolist.api.v1.permissions import IsTodoOwner
# Create your views here.


class TaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["name"]
    ordering_fields = ["due_date", "created_at", "is_completed"]
    permission_classes = [IsAuthenticated, IsTodoOwner]

    queryset = Task.objects.none()

    def get_queryset(self):
        todo_list_id = self.kwargs["list_id"]
        return Task.objects.filter(todo__owner=self.request.user, todo=todo_list_id)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TaskCreateSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        todo_list_id = self.kwargs["list_id"]
        serializer.save(todo_id=todo_list_id)


class TaskListDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, IsTodoOwner]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TaskSerializer
        return TaskUpdateSerializer
