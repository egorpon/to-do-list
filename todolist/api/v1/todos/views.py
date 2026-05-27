from rest_framework import generics
from ....todos.models import TodoList
from .serializers import (
    TodoListSerializer,
    TodoListCreateUpdateSerializer,
    TodoListDetailSerializer,
)
# Create your views here.


class TodoListCreateAPIView(generics.ListCreateAPIView):
    queryset = TodoList.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TodoListCreateUpdateSerializer
        return TodoListSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TodoListDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TodoList.objects.all()
    lookup_field = "id"

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TodoListDetailSerializer
        return TodoListCreateUpdateSerializer
