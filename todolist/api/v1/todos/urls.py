from django.urls import path
from .views import (
    TodoListCreateAPIView,
    TodoListDetailUpdateDeleteAPIView
)
from todolist.api.v1.tasks.views import TaskListCreateAPIView

urlpatterns = [
    path("", view=TodoListCreateAPIView.as_view(), name="list"),
    path("<int:id>/", view=TodoListDetailUpdateDeleteAPIView.as_view(), name="list-detail"),
    path('<int:list_id>/tasks/', view=TaskListCreateAPIView.as_view(), name='todo-task-list'),


]
