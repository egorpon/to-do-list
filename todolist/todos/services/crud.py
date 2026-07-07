from todolist.todos.models import TodoList, User
from django.db import transaction
from typing import Any


@transaction.atomic
def todolist_create(*, name: str, owner: User, description: str = "") -> TodoList:

    obj = TodoList(name=name, description=description, owner=owner)

    obj.full_clean()
    obj.save()

    return obj


@transaction.atomic
def todolist_update(*, data: dict[str, Any], todo: TodoList) -> TodoList:

    for field, value in data.items():
        setattr(todo, field, value)

    todo.full_clean()
    todo.save()

    return todo
