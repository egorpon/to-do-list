from django.urls import path, include


urlpatterns = [
    path("todos/", include("todolist.api.v1.todos.urls")),
    path("tasks/", include("todolist.api.v1.tasks.urls")),
]
