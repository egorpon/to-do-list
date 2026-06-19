from django.test import TestCase
from todolist.todos.selectors import get_todo
from todolist.api.v1.exceptions import TodoNotFound
from todolist.todos.tests.factories import UserFactory


class TodoSelectorTest(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_raise_todo_not_found_if_get_todo_failed(self):
        with self.assertRaises(TodoNotFound):
            get_todo(todo_id=12321, owner=self.user)
