from django.test import TestCase
from todolist.todos.services import todolist_create, todolist_update
from todolist.todos.tests.factories import UserFactory, TodoListFactory
from todolist.todos.models import TodoList


class TodoServiceTest(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_todolist_create_saves_todolist_to_db(self):
        todo = todolist_create(name="cleaning", owner=self.user)
        self.assertEqual(TodoList.objects.count(), 1)
        self.assertEqual(todo.name, "cleaning")

    def test_todolist_update_changes_field(self):
        todo = TodoListFactory(owner=self.user)
        updated_todo = todolist_update(data={"name": "updated field"}, todo=todo)
        self.assertEqual(updated_todo.name, "updated field")
        todo.refresh_from_db()
        self.assertEqual(todo.name, "updated field")
