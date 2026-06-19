from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler
from todolist.api.v1.exceptions import TodoNotFound, TaskNotFound


def custom_exception_handler(exc, ctx):
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(detail=as_serializer_error(exc))

    if isinstance(exc, TodoNotFound):
        exc = exceptions.NotFound(detail="Todo list not found.")
    
    if isinstance(exc, TodoNotFound):
        exc = exceptions.NotFound(detail="Task not found.")
    
    response = exception_handler(exc, ctx)

    return response
