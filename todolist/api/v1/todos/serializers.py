from rest_framework import serializers
from todolist.todos.models import TodoList
from todolist.api.v1.mixins import (
    ReadOnlySerializerMixin,
    CreateOnlySerializerMixin,
    UpdateOnlySerializerMixin,
)


class TodoStatsDisplaySerializer(ReadOnlySerializerMixin, serializers.Serializer):
    tasks_count = serializers.IntegerField(default=0)
    tasks_done = serializers.IntegerField(default=0)
    tasks_pending = serializers.IntegerField(default=0)
    upcoming_tasks = serializers.IntegerField(default=0)
    overdue_tasks = serializers.IntegerField(default=0)


class TodoDisplaySerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
    stats = TodoStatsDisplaySerializer(source="*")

    class Meta:
        model = TodoList
        fields = ("id", "name", "description", "created_at", "owner", "stats")


class TodoCreateSerializer(CreateOnlySerializerMixin, serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)


class TodoUpdateSerializer(UpdateOnlySerializerMixin, serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
