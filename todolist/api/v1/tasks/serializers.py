from rest_framework import serializers
from todolist.tasks.models import Task
from todolist.api.v1.mixins import (
    ReadOnlySerializerMixin,
    CreateOnlySerializerMixin,
    UpdateOnlySerializerMixin,
)


class TaskDisplaySerializer(ReadOnlySerializerMixin, serializers.ModelSerializer):
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
            "todo_id",
        )


class FilterSerializer(serializers.Serializer):
    is_completed = serializers.BooleanField(required=False)
    due_date = serializers.DateTimeField(required=False)


class TaskCreateSerializer(CreateOnlySerializerMixin, serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, required=False)
    due_date = serializers.DateTimeField(allow_null=True, required=False)


class TaskUpdateSerializer(UpdateOnlySerializerMixin, serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, required=False)
    due_date = serializers.DateTimeField(allow_null=True, required=False)
    is_completed = serializers.BooleanField()
