from rest_framework import generics
from todolist.todos.models import TodoList
from .serializers import (
    TodoListSerializer,
    TodoListCreateUpdateSerializer,
)
from rest_framework.permissions import IsAuthenticated
from todolist.api.v1.permissions import IsOwner
from todolist.api.v1.pagination import TodoListPagination
# Create your views here.

class TodoListCreateAPIView(generics.ListCreateAPIView):
    queryset = TodoList.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = TodoListPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TodoListCreateUpdateSerializer
        return TodoListSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class TodoListDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TodoList.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, IsOwner]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TodoListSerializer
        return TodoListCreateUpdateSerializer
