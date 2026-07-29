from rest_framework.generics import GenericAPIView
from .serializers import (
    TodoDisplaySerializer,
    TodoCreateSerializer,
    TodoUpdateSerializer,
)
from rest_framework.permissions import IsAuthenticated
from todolist.api.v1.pagination import PageNumberPagination
from todolist.todos.selectors import todos_list, get_todo
from todolist.todos.services.crud import todolist_create, todolist_update
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator
from django.core.cache import cache
# Create your views here.


class TodoListAPI(GenericAPIView):
    output_serializer_class = TodoDisplaySerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        tags=["todolist"],
        responses={status.HTTP_200_OK: TodoDisplaySerializer(many=True)},
    )
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request):
        page_number = request.query_params.get("page", 1)
        page_size = request.query_params.get("page_size", 5)
        cache_key = f"todos:user:{request.user.id}:page:{page_number}:size:{page_size}"

        data = cache.get(cache_key)
        if data is not None:
            return Response(data)

        import time

        time.sleep(5)

        todos = todos_list(owner=request.user)
        page = self.paginate_queryset(todos)
        serializer = self.output_serializer_class(page, many=True)
        response = self.get_paginated_response(serializer.data)

        cache.set(cache_key, response.data, 60 * 15)
        return response


class TodoDetailAPI(GenericAPIView):
    output_serializer_class = TodoDisplaySerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        tags=["todolist"], responses={status.HTTP_200_OK: TodoDisplaySerializer}
    )
    def get(self, request, todo_id):

        todo = get_todo(todo_id=todo_id, owner=request.user)
        serializer = self.output_serializer_class(todo)
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
