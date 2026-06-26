from django.test import TestCase
from todolist.tasks.selectors import get_task, tasks_list
from todolist.api.v1.exceptions import TodoAppBaseError
from todolist.todos.tests.factories import UserFactory, TodoListFactory
from todolist.tasks.tests.factories import TaskFactory


class TaskSelectorTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.todo = TodoListFactory(owner=self.user)
        self.task_1 = TaskFactory(todo=self.todo)
        self.task_2 = TaskFactory(todo=self.todo)

    def test_tasks_list_returns_tasks_if_user_is_todo_owner(self):
        tasks = tasks_list(todo_id=self.todo.id, user=self.user)
        self.assertQuerySetEqual(tasks, [self.task_1, self.task_2], ordered=False)

    def test_tasks_list_returns_empty_if_user_is_not_todo_owner(self):
        tasks = tasks_list(todo_id=self.todo.id, user=self.other_user)
        self.assertQuerySetEqual(tasks, [])

    def test_get_task_returns_task_if_found_and_user_is_todo_owner(self):
        task = get_task(task_id=self.task_1.id)
        self.assertEqual(task.id, self.task_1.id)

    def test_get_task_raises_error_if_task_not_found(self):
        with self.assertRaises(TodoAppBaseError):
            get_task(task_id=999)

