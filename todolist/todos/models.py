from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class TodoList(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="todolists")

    def __str__(self):
        return self.name
