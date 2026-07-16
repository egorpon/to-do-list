from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler
from todolist.api.v1.exceptions import TodoAppBaseError

from rest_framework.response import Response


def custom_exception_handler(exc, ctx):
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(detail=as_serializer_error(exc))

    if isinstance(exc, TodoAppBaseError):
        data = {"message": str(exc), "extra": exc.extra}
        return Response(data, status=exc.status_code)

    return exception_handler(exc, ctx)
