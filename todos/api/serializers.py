from rest_framework import serializers
from ..models import TodoList
from tasks.api.serializers import TaskSerializer
from django.utils import timezone


class TodoListSerializer(serializers.ModelSerializer):
    tasks_count = serializers.SerializerMethodField()
    tasks_done = serializers.SerializerMethodField()

    def get_tasks_count(self, obj):
        return obj.tasks.count()

    def get_tasks_done(self, obj):
        return obj.tasks.filter(is_completed=True).count()

    class Meta:
        model = TodoList
        fields = ("id", "name", "created_at", "tasks_count", "tasks_done")


class TodoListCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields = ("name", "description")


class TodoListDetailSerializer(serializers.ModelSerializer):
    tasks_count = serializers.SerializerMethodField()
    tasks_done = serializers.SerializerMethodField()
    upcoming_tasks = serializers.SerializerMethodField()
    tasks = TaskSerializer(many=True, read_only=True)

    def get_tasks_count(self, obj):
        return obj.tasks.count()

    def get_tasks_done(self, obj):
        return obj.tasks.filter(is_completed=True).count()

    def get_upcoming_tasks(self, obj):
        return obj.tasks.filter(is_completed=False, due_date__gt=timezone.now()).count()

    class Meta:
        model = TodoList
        fields = (
            "id",
            "name",
            "description",
            "tasks_count",
            "tasks_done",
            "upcoming_tasks",
            "tasks",
        )
