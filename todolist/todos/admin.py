from django.contrib import admin
from .models import TodoList
# Register your models here.

class TodoListAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user
        return super().save_model(request, obj, form, change)

admin.site.register(TodoList, TodoListAdmin)