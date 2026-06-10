from rest_framework.views import APIView
from .serializers import (
    TodoListSerializer,
    TodoListCreateUpdateSerializer,
)
from todolist.api.v1.permissions import IsOwner
from todolist.api.v1.pagination import get_paginated_response, LimitOffsetPagination
from todolist.todos.selectors import todos_list, get_todo
from todolist.todos.services import todolist_create, todolist_update
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
# Create your views here.


class TodoListAPI(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(name="limit", type=int, required=False),
            OpenApiParameter(name="offset", type=int, required=False),
        ],
        responses={200: TodoListSerializer(many=True)},
    )
    def get(self, request):

        todos = todos_list(owner=self.request.user)

        return get_paginated_response(
            pagination_class=LimitOffsetPagination,
            serializer_class=TodoListSerializer,
            queryset=todos,
            request=request,
            view=self,
        )


class TodoDetailAPI(APIView):
    @extend_schema(responses={200: TodoListSerializer})
    def get(self, request, todo_id):

        todos = get_todo(todo_id=todo_id, owner=self.request.user)

        serializer = TodoListSerializer(todos)
        return Response(serializer.data)


class TodoCreateAPI(APIView):
    @extend_schema(
        request=TodoListCreateUpdateSerializer, responses={200: TodoListSerializer}
    )
    def post(self, request):
        serializer = TodoListCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        todolist_create(**serializer.validated_data, owner=self.request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TodoUpdateAPI(APIView):
    @extend_schema(
        request=TodoListCreateUpdateSerializer, responses={200: TodoListSerializer}
    )
    def patch(self, request, todo_id):
        todo = get_todo(todo_id, owner=self.request.user)

        serializer = TodoListCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        todolist_update(data = serializer.validated_data, todo=todo)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TodoDeleteAPI(APIView):
    @extend_schema(responses={204: None})
    def delete(self, request, todo_id):
        todo = get_todo(todo_id, owner=self.request.user)

        todo.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
