from .serializers import (
    TaskDisplaySerializer,
    FilterSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
)
from rest_framework import generics, filters
from rest_framework.views import APIView
from todolist.tasks.models import Task
from todolist.tasks.filters import TaskFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from todolist.api.v1.permissions import IsTodoOwner
from todolist.tasks.selectors import tasks_list
from todolist.api.v1.pagination import get_paginated_response, LimitOffsetPagination
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from datetime import datetime
# Create your views here.


class TaskListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTodoOwner]

    @extend_schema(
        parameters=[
            OpenApiParameter(name="limit", type=int, required=False),
            OpenApiParameter(name="offset", type=int, required=False),
            OpenApiParameter(name="search", type=str, required=False),
            OpenApiParameter(name="ordering", type=str, required=False),
            OpenApiParameter(name="is_completed", type=bool, required=False),
            OpenApiParameter(name="due_date_after", type=datetime, required=False),
            OpenApiParameter(name="due_date_before", type=datetime, required=False),
        ],
        responses={200: TaskDisplaySerializer(many=True)},
    )
    def get(self, request, todo_id):
        filters_serializer = FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        tasks = tasks_list(
            filters=filters_serializer.validated_data,
            todo_id=todo_id,
            user=self.request.user,
        )

        return get_paginated_response(
            pagination_class=LimitOffsetPagination,
            serializer_class=TaskDisplaySerializer,
            queryset=tasks,
            request=request,
            view=self,
        )


class TaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TaskDisplaySerializer
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
        return TaskDisplaySerializer

    def perform_create(self, serializer):
        todo_list_id = self.kwargs["list_id"]
        serializer.save(todo_id=todo_list_id)


class TaskListDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, IsTodoOwner]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TaskDisplaySerializer
        return TaskUpdateSerializer
