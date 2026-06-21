from django.urls import path
from .views import TaskDetailAPI, TaskUpdateAPI, TaskDeleteAPI

urlpatterns = [
    path(
        "<int:task_id>/",
        view=TaskDetailAPI.as_view(),
        name="task-detail",
    ),
    path(
        "<int:task_id>/update",
        view=TaskUpdateAPI.as_view(),
        name="task-update",
    ),
    path(
        "<int:task_id>/delete",
        view=TaskDeleteAPI.as_view(),
        name="task-delete",
    ),
]
