from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class TodoList(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE, related_name="todolists"
    )

    def __str__(self):
        return self.name


class ReminderLog(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING"
        SUCCESS = "SUCCESS"
        FAILED = "FAILED"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reminder_logs"
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "user",
                    "created_at",
                ),
                name="unique_daily_reminder",
            )
        ]

    def __str__(self):
        return f"Reminder for {self.user} on {self.created_at}: {self.status}"
