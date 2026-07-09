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
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reminder_logs"
    )
    date = models.DateField(blank=True, null=False)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    error_message = models.TextField(blank=True, default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "user",
                    "date",
                ),
                name="unique_daily_summary",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.date}: {self.status}"
