from django.db import models
from todos.models import TodoList


# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(blank=True, null=True)

    todo = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return self.name
