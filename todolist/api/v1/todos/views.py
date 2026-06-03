from rest_framework import generics
from todolist.todos.models import TodoList
from .serializers import (
    TodoListSerializer,
    TodoListCreateUpdateSerializer,
)
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class TodoListCreateAPIView(generics.ListCreateAPIView):
    queryset = TodoList.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TodoListCreateUpdateSerializer
        return TodoListSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
    
    


class TodoListDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TodoList.objects.all()
    lookup_field = "id"

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TodoListSerializer
        return TodoListCreateUpdateSerializer

