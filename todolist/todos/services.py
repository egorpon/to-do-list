from todolist.todos.models import TodoList, User
from django.shortcuts import get_object_or_404
from django.db import transaction


@transaction.atomic
def todolist_create(*, name: str, description: str, owner: User) -> TodoList:

    obj = TodoList(name=name, description=description, owner=owner)

    obj.full_clean()
    obj.save()

    return obj


@transaction.atomic
def todolist_update(*, data: dict, todo: TodoList) -> TodoList:

    for field, value in data.items():
        setattr(todo,field,value)

    todo.full_clean()
    todo.save()

    return todo
