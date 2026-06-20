from rest_framework.permissions import BasePermission
from todolist.todos.models import TodoList


class IsTodoOwner(BasePermission):
    message = "You do not have permission to perfom this action."

    def has_permission(self, request, view):
        todo_id = view.kwargs.get("todo_id")
        if todo_id:
            return TodoList.objects.filter(id=todo_id, owner=request.user).exists()

        return True

    def has_object_permission(self, request, view, obj):
        return obj.todo.owner == request.user
