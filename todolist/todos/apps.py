from django.apps import AppConfig


class TodosConfig(AppConfig):
    name = "todolist.todos"


    def ready(self):
        from . import signals