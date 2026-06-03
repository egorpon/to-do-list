import factory
from todolist.tasks.models import Task

class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task
    name = factory.Sequence(lambda x: f'task {x}')
