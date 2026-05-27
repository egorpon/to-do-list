from rest_framework import serializers
from todolist.todos.models import TodoList
from todolist.api.v1.tasks.serializers import TaskSerializer
from django.utils import timezone


class TodoListSerializer(serializers.ModelSerializer):
    tasks_count = serializers.SerializerMethodField()
    tasks_done = serializers.SerializerMethodField()
    tasks_pending = serializers.SerializerMethodField()
    upcoming_tasks = serializers.SerializerMethodField()

    def get_tasks_count(self, obj):
        return obj.tasks.count()

    def get_tasks_done(self, obj):
        return obj.tasks.filter(is_completed=True).count()

    def get_tasks_pending(self, obj):
        return obj.tasks.filter(is_completed=False).count()
    
    def get_upcoming_tasks(self, obj):
        return obj.tasks.filter(is_completed=False, due_date__gt=timezone.now()).count()

    class Meta:
        model = TodoList
        fields = ("id", "name", "created_at", "tasks_count", "tasks_done", "tasks_pending", "upcoming_tasks")


class TodoListCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields = ("name", "description")
