from django.urls import path
from .views import (
    TodoListCreateAPIView,
    TodoListDetailUpdateDeleteAPIView
)

urlpatterns = [
    path("", view=TodoListCreateAPIView.as_view(), name="list"),
    path("<int:id>/", view=TodoListDetailUpdateDeleteAPIView.as_view(), name="list-detail"),

]
