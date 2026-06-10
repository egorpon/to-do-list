from todolist.todos.models import TodoList
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404


def todos_list(*, owner=None) -> QuerySet[TodoList]:

    return TodoList.objects.filter(owner=owner)

def get_todo(todo_id, owner) -> TodoList:

    todo = get_object_or_404(TodoList, id=todo_id, owner=owner)

    return todo
