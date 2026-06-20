from django.test import TestCase
from todolist.todos.selectors import get_todo, todos_list
from todolist.api.v1.exceptions import TodoAppBaseError
from todolist.todos.tests.factories import UserFactory, TodoListFactory


class TodoSelectorTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.todo_1 = TodoListFactory(owner=self.user)
        self.todo_2 = TodoListFactory(owner=self.user)

    def test_todos_list_returns_todos_if_user_is_owner(self):
        todos = todos_list(owner=self.user)
        self.assertQuerySetEqual(todos, [self.todo_1, self.todo_2], ordered=False)

    def test_todos_list_returns_empty_if_user_is_not_owner(self):
        todos = todos_list(owner=self.other_user)
        self.assertQuerySetEqual(todos, [])

    def test_get_todo_returns_todo_if_found_and_user_is_owner(self):
        todo = get_todo(todo_id=self.todo_1.id, owner=self.user)
        self.assertEqual(todo.id, self.todo_1.id)

    def test_get_todo_raises_error_if_todo_not_found(self):
        with self.assertRaises(TodoAppBaseError):
            get_todo(todo_id=999, owner=self.user)

    def test_get_todo_raises_error_if_user_is_not_owner(self):
        with self.assertRaises(TodoAppBaseError):
            get_todo(todo_id=self.todo_1.id, owner=self.other_user)
