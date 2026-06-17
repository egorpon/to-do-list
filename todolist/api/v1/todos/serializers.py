from rest_framework import serializers
from todolist.todos.models import TodoList
from todolist.api.v1.mixins import (
    ReadOnlySerializerMixin,
    CreateOnlySerializerMixin,
    UpdateOnlySerializerMixin,
)


class TodoDisplaySerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    stats = serializers.SerializerMethodField()

    class Meta:
        model = TodoList
        fields = ("id", "name", "description", "created_at", "owner", "stats")

    def get_stats(self, obj):

        return {
            "tasks_count": getattr(obj, "tasks_count", 0),
            "tasks_done": getattr(obj, "tasks_done", 0),
            "tasks_pending": getattr(obj, "tasks_pending", 0),
            "upcoming_tasks": getattr(obj, "upcoming_tasks", 0),
            "overdue_tasks": getattr(obj, "overdue_tasks", 0),
        }


class TodoCreateSerializer(CreateOnlySerializerMixin, serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)


class TodoUpdateSerializer(UpdateOnlySerializerMixin, serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
