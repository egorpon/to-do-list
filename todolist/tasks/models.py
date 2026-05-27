from django.db import models
from todolist.todos.models import TodoList
from django.core.exceptions import ValidationError
from django.utils import timezone


# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    todo = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return self.name

    def clean(self):
        if timezone.now() >= self.due_date:
            raise ValidationError("Due date cannot be in the past")
