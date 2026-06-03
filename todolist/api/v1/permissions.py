from rest_framework.permissions import BasePermission
from todolist.todos.models import TodoList
from todolist.tasks.models import Task


class IsOwner(BasePermission):
    message = "You do not have permission to perfom this action."

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsTodoOwner(BasePermission):
    message = "You do not have permission to perfom this action."

    def has_permission(self, request, view):
        list_id = view.kwargs.get("list_id")
        if list_id:
            return TodoList.objects.filter(id=list_id, owner=request.user).exists()

        return True

    def has_object_permission(self, request, view, obj):
        return obj.todo.owner == request.user
