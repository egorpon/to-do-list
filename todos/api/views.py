from rest_framework import generics
from ..models import TodoList
from .serializers import (
    TodoListSerializer,
    TodoListCreateUpdateSerializer,
    TodoListDetailSerializer,
)
# Create your views here.


class TodoListAPIView(generics.ListAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer


class TodoListDetailAPIView(generics.RetrieveAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoListDetailSerializer
    lookup_field = "id"


class TodoListCreateAPIView(generics.CreateAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoListCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TodoListUpdateAPIView(generics.UpdateAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoListCreateUpdateSerializer
    lookup_field = "id"


class TodoListDeleteAPIView(generics.DestroyAPIView):
    queryset = TodoList.objects.all()
    lookup_field = "id"

