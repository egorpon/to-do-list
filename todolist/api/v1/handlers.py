from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler


def custom_exception_handler(exc, ctx):
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(detail=as_serializer_error(exc))
    
    response = exception_handler(exc, ctx)

    return response
