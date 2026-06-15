from django.urls import path
from .views import (
    TodoListAPI,
    TodoDetailAPI,
    TodoCreateAPI,
    TodoUpdateAPI,
    TodoDeleteAPI,
)
from todolist.api.v1.tasks.views import TaskListCreateAPIView, TaskListAPIView

urlpatterns = [
    path("", view=TodoListAPI.as_view(), name="list"),
    path(
        "<int:todo_id>/",
        view=TodoDetailAPI.as_view(),
        name="detail",
    ),
    path("create/", view=TodoCreateAPI.as_view(), name="create"),
    path(
        "<int:todo_id>/update/",
        view=TodoUpdateAPI.as_view(),
        name="update",
    ),
    path(
        "<int:todo_id>/delete/",
        view=TodoDeleteAPI.as_view(),
        name="delete",
    ),
    path(
        "<int:todo_id>/tasks/",
        view=TaskListAPIView.as_view(),
        name="todo-task-list",
    ),
]
