from rest_framework.generics import GenericAPIView
from .serializers import (
    TodoDisplaySerializer,
    TodoCreateSerializer,
    TodoUpdateSerializer,
)
from rest_framework.permissions import IsAuthenticated
from todolist.api.v1.pagination import PageNumberPagination
from todolist.todos.selectors import todos_list, get_todo
from todolist.todos.services import todolist_create, todolist_update
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
# Create your views here.


class TodoListAPI(GenericAPIView):
    output_serializer_class = TodoDisplaySerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        tags=["todolist"],
        responses={status.HTTP_200_OK: TodoDisplaySerializer(many=True)},
    )
    def get(self, request):

        todos = todos_list(owner=request.user)
        page = self.paginate_queryset(todos)
        if page is not None:
            serializer = self.output_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.output_serializer_class(todos)
        return Response(serializer.data)


class TodoDetailAPI(GenericAPIView):
    output_serializer_class = TodoDisplaySerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        tags=["todolist"], responses={status.HTTP_200_OK: TodoDisplaySerializer}
    )
    def get(self, request, todo_id):

        todos = get_todo(todo_id=todo_id, owner=request.user)

        serializer = self.output_serializer_class(todos)
        return Response(serializer.data)


class TodoCreateAPI(GenericAPIView):
    input_serializer_class = TodoCreateSerializer
    output_serializer_class = TodoDisplaySerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        tags=["todolist"],
        request=TodoCreateSerializer,
        responses={status.HTTP_201_CREATED: TodoDisplaySerializer},
    )
    def post(self, request):
        serializer = self.input_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        todo = todolist_create(**serializer.validated_data, owner=request.user)

        return Response(
            self.output_serializer_class(todo).data, status=status.HTTP_201_CREATED
        )


class TodoUpdateAPI(GenericAPIView):
    input_serializer_class = TodoUpdateSerializer
    output_serializer_class = TodoDisplaySerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        tags=["todolist"],
        request=TodoUpdateSerializer,
        responses={status.HTTP_200_OK: TodoDisplaySerializer},
    )
    def patch(self, request, todo_id):
        todo = get_todo(todo_id, owner=request.user)

        serializer = self.input_serializer_class(
            instance=todo, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        todo = todolist_update(data=serializer.validated_data, todo=todo)

        return Response(self.output_serializer_class(todo).data)


class TodoDeleteAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(tags=["todolist"], responses={status.HTTP_204_NO_CONTENT: None})
    def delete(self, request, todo_id):
        todo = get_todo(todo_id, owner=request.user)

        todo.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
