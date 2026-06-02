from rest_framework import serializers
from todolist.tasks.models import Task
from django.utils import timezone


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
            "due_date",
            "is_completed",
            "todo_id"
        )


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("name", "description", "due_date")

    def validate_due_date(self, value):
        if value and timezone.now() >= value:
            raise serializers.ValidationError("Due date cannot be in the past")
        return value


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("name", "description", "due_date", "is_completed")

    def validate_due_date(self, value):
        if value and timezone.now() >= value:
            raise serializers.ValidationError("Due date cannot be in the past")
        return value
