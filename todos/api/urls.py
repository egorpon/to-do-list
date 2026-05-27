from django.urls import path
from .views import (
    TodoListCreateAPIView,
    TodoListDetailUpdateDeleteAPIView
)

urlpatterns = [
    path("lists/", view=TodoListCreateAPIView.as_view(), name="list"),
    path("lists/<int:id>/", view=TodoListDetailUpdateDeleteAPIView.as_view(), name="list-detail"),

]
