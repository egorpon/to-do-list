from rest_framework import serializers
from todolist.todos.models import TodoList
from django.utils import timezone


class TodoListSerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField()

    def get_stats(self, obj):
        tasks = obj.tasks.all()
        return {
            "tasks_count": tasks.count(),
            "tasks_done": tasks.filter(is_completed=True).count(),
            "tasks_pending": tasks.filter(is_completed=False).count(),
            "upcoming_tasks": tasks.filter(
                is_completed=False, due_date__gt=timezone.now()
            ).count(),
            "overdue_tasks": tasks.filter(
                is_completed=False, due_date__lt=timezone.now()
            ).count(),
        }

    class Meta:
        model = TodoList
        fields = (
            "id",
            "name",
            "description",
            "created_at",
            "owner",
            "stats",
        )


class TodoListCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields = ("name", "description")
