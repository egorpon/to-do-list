from django.urls import path, include


urlpatterns = [
    path("v1/", include("todolist.api.v1.urls")),
]
