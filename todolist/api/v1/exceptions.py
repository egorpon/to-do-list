from rest_framework import status


class TodoAppBaseError(Exception):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str, extra: dict | None = None):
        self.extra = extra or {}
        super().__init__(message)


class TodoAppNotFound(TodoAppBaseError):
    status_code = status.HTTP_404_NOT_FOUND
