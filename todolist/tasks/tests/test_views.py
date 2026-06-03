from django.test import TestCase
from .factories import TaskFactory
from todolist.todos.tests.factories import TodoListFactory
# Create your tests here.


class TaskViewTest(TestCase):
    def setUp(self):
        todo = TodoListFactory()
        task = TaskFactory(todo=todo)
