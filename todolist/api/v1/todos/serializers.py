from rest_framework import serializers


class TodoListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    created_at = serializers.DateTimeField()
    owner = serializers.IntegerField(source="owner.id")
    stats = serializers.SerializerMethodField()

    def get_stats(self, obj):

        return {
            "tasks_count": getattr(obj, "tasks_count", 0),
            "tasks_done": getattr(obj, "tasks_done", 0),
            "tasks_pending": getattr(obj, "tasks_pending", 0),
            "upcoming_tasks": getattr(obj, "upcoming_tasks", 0),
            "overdue_tasks": getattr(obj, "overdue_tasks", 0),
        }


class TodoListCreateUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
