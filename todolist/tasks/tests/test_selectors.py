from django.test import TestCase
from todolist.tasks.selectors import get_task
from todolist.api.v1.exceptions import TaskNotFound
from todolist.todos.tests.factories import UserFactory


class TodoSelectorTest(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_raise_todo_not_found_if_get_todo_failed(self):
        with self.assertRaises(TaskNotFound):
            get_task(task_id=12321, user=self.user)
