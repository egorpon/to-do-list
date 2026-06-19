class TodoAppBaseError(Exception):
    def __init__(self, message: str, extra: dict | None = None):
        self.extra = extra or {}
        super().__init__(message)
