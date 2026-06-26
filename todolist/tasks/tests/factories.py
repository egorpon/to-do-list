import factory
from todolist.tasks.models import Task
from todolist.todos.tests.factories import TodoListFactory


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    name = factory.Sequence(lambda x: f"task {x}")
    description = ""
    due_date = None
    is_completed = False
    todo = factory.SubFactory(TodoListFactory)
