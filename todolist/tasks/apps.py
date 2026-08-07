from django.apps import AppConfig


class TasksConfig(AppConfig):
    name = "todolist.tasks"

    def ready(self):
            import todolist.tasks.signals
