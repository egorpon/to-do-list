import factory
from django.contrib.auth.models import User
from todolist.todos.models import TodoList


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda x: f"user_{x}")


class TodoListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TodoList

    name = factory.Sequence(lambda x: f"to-do-list {x}")
    description = ""
    owner = factory.SubFactory(UserFactory)
