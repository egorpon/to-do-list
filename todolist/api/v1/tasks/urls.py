from django.urls import path
from .views import TaskListDetailUpdateDeleteAPIView

urlpatterns = [
    path(
        "<int:id>/",
        view=TaskListDetailUpdateDeleteAPIView.as_view(),
        name="task-detail",
    )
]
