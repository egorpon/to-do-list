from django.test import TestCase
from todolist.tasks.services import task_create, task_update
from todolist.todos.tests.factories import UserFactory, TodoListFactory
from todolist.tasks.tests.factories import TaskFactory
from todolist.tasks.models import Task
from django.utils import timezone
from django.core.exceptions import ValidationError


class TaskServiceTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.todo = TodoListFactory(owner=self.user)

    def test_task_create_saves_task_to_db(self):
        task = task_create(name="wash the dishes", todo_id=self.todo.id)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(task.name, "wash the dishes")

    def test_task_create_raises_error_if_due_date_is_in_the_past(self):
        with self.assertRaises(ValidationError):
            task_create(
                name="wash the dishes",
                due_date=timezone.now() - timezone.timedelta(days=1),
                todo_id=self.todo.id,
            )
        self.assertEqual(Task.objects.count(), 0)

    def test_task_update_changes_field(self):
        task = TaskFactory(todo=self.todo)
        updated_task = task_update(data={"name": "updated field"}, task=task)
        self.assertEqual(updated_task.name, "updated field")
        task.refresh_from_db()
        self.assertEqual(task.name, "updated field")

    def test_task_update_raises_error_if_due_date_is_in_the_past(self):
        task = TaskFactory(name="updated field", todo=self.todo)
        with self.assertRaises(ValidationError):
            task_update(
                data={
                    "name": "test",
                    "due_date": timezone.now() - timezone.timedelta(days=1),
                },
                task=task,
            )
        task.refresh_from_db()
        self.assertEqual(task.name, "updated field")
