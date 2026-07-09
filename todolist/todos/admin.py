from django.contrib import admin
from .models import TodoList
from todolist.tasks.models import Task
from todolist.todos.models import ReminderLog
# Register your models here.


class TaskInline(admin.StackedInline):
    model = Task
    extra = 1


@admin.register(TodoList)
class TodoListAdmin(admin.ModelAdmin):
    inlines = [TaskInline]
    list_display = ["id", "name", "owner"]
    list_filter = ["owner"]
    search_fields = ["name"]

    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user
        return super().save_model(request, obj, form, change)


@admin.register(ReminderLog)
class ReminderLogAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "date", "status"]
    list_display_links = ["id"]
    list_filter = ["status", "date"]
    search_fields = ["user"]
