from django.urls import path
from .views import (
    TodoListAPI,
    TodoDetailAPI,
    TodoCreateAPI,
    TodoUpdateAPI,
    TodoDeleteAPI,
)
from todolist.api.v1.tasks.views import TaskListAPI, TaskCreateAPI

urlpatterns = [
    path("", view=TodoListAPI.as_view(), name="todo-list"),
    path(
        "<int:todo_id>/",
        view=TodoDetailAPI.as_view(),
        name="todo-detail",
    ),
    path("create/", view=TodoCreateAPI.as_view(), name="todo-create"),
    path(
        "<int:todo_id>/update/",
        view=TodoUpdateAPI.as_view(),
        name="todo-update",
    ),
    path(
        "<int:todo_id>/delete/",
        view=TodoDeleteAPI.as_view(),
        name="todo-delete",
    ),
    path(
        "<int:todo_id>/tasks/",
        view=TaskListAPI.as_view(),
        name="todo-task-list",
    ),
    path(
        "<int:todo_id>/tasks/create",
        view=TaskCreateAPI.as_view(),
        name="todo-task-create",
    ),
]
