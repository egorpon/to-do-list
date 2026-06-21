from .serializers import (
    TaskDisplaySerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
)
from rest_framework import filters
from rest_framework.generics import GenericAPIView
from todolist.tasks.filters import TaskFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from todolist.api.v1.permissions import IsTodoOwner
from todolist.tasks.selectors import tasks_list, get_task
from todolist.tasks.services import task_create, task_update
from rest_framework import status
from drf_spectacular.utils import extend_schema
from todolist.api.v1.pagination import PageNumberPagination
from rest_framework.response import Response
# Create your views here.


class TaskListAPI(GenericAPIView):
    output_serializer_class = TaskDisplaySerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        IsAuthenticated,
        IsTodoOwner,
    )
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = TaskFilter
    search_fields = ["name"]
    ordering_fields = ["name", "due_date", "created_at", "is_completed"]

    @extend_schema(
        tags=["tasks"],
        responses={status.HTTP_200_OK: TaskDisplaySerializer(many=True)},
    )
    def get(self, request, todo_id):
        tasks = tasks_list(
            todo_id=todo_id,
            user=request.user,
        )

        tasks = self.filter_queryset(tasks)

        page = self.paginate_queryset(tasks)

        serializer = self.output_serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)


class TaskDetailAPI(GenericAPIView):
    output_serializer_class = TaskDisplaySerializer
    permission_classes = (
        IsAuthenticated,
        IsTodoOwner,
    )

    @extend_schema(
        tags=["tasks"],
        responses={status.HTTP_200_OK: TaskDisplaySerializer},
    )
    def get(self, request, task_id):

        tasks = get_task(
            task_id=task_id,
            user=request.user,
        )

        serializer = self.output_serializer_class(tasks)
        return Response(serializer.data)


class TaskCreateAPI(GenericAPIView):
    input_serializer_class = TaskCreateSerializer
    output_serializer_class = TaskDisplaySerializer
    permission_classes = (
        IsAuthenticated,
        IsTodoOwner,
    )

    @extend_schema(
        tags=["tasks"],
        request=TaskCreateSerializer,
        responses={status.HTTP_201_CREATED: TaskDisplaySerializer()},
    )
    def post(self, request, todo_id):
        serializer = self.input_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = task_create(**serializer.validated_data, todo_id=todo_id)

        return Response(self.output_serializer_class(task).data)


class TaskUpdateAPI(GenericAPIView):
    input_serializer_class = TaskUpdateSerializer
    output_serializer_class = TaskDisplaySerializer
    permission_classes = (
        IsAuthenticated,
        IsTodoOwner,
    )

    @extend_schema(
        tags=["tasks"],
        request=TaskUpdateSerializer,
        responses={201: TaskDisplaySerializer()},
    )
    def patch(self, request, task_id):
        task = get_task(task_id=task_id, user=request.user)
        serializer = self.input_serializer_class(
            instance=task, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        task = task_update(data=serializer.validated_data, task=task)

        return Response(self.output_serializer_class(task).data)


class TaskDeleteAPI(GenericAPIView):
    permission_classes = (
        IsAuthenticated,
        IsTodoOwner,
    )

    @extend_schema(tags=["tasks"], responses={status.HTTP_204_NO_CONTENT: None})
    def delete(self, request, task_id):
        task = get_task(task_id=task_id, user=request.user)

        task.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
