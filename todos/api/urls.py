from django.urls import path
from .views import TodoListAPIView, TodoListCreateAPIView, TodoListDetailAPIView, TodoListUpdateAPIView, TodoListDeleteAPIView

urlpatterns = [
    path("lists/", view=TodoListAPIView.as_view()),
    path("lists/<int:id>/", view=TodoListDetailAPIView.as_view()),
    path("lists/create/", view=TodoListCreateAPIView.as_view()),
    path("lists/<int:id>/update/", view=TodoListUpdateAPIView.as_view()),
    path("lists/<int:id>/delete/", view=TodoListDeleteAPIView.as_view()),
]
