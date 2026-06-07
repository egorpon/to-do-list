from django.contrib import admin
from .models import TodoList
from todolist.tasks.models import Task
# Register your models here.


class TaskInline(admin.StackedInline):
    model = Task
    extra = 1


class TodoListAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user
        return super().save_model(request, obj, form, change)

    inlines = [TaskInline]


admin.site.register(TodoList, TodoListAdmin)
