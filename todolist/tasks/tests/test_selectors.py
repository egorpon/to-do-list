from django.test import TestCase
from todolist.tasks.selectors import (
    get_task,
    tasks_list,
    get_tasks_stats,
    get_overdue_tasks,
    get_upcoming_tasks_this_week,
    get_completed_tasks_this_week,
    get_users_with_active_tasks,
)
from todolist.api.v1.exceptions import TodoAppBaseError
from todolist.todos.tests.factories import UserFactory, TodoListFactory
from todolist.tasks.tests.factories import TaskFactory
from django.utils import timezone


class TaskSelectorTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.todo = TodoListFactory(owner=self.user)

        self.other_user = UserFactory()

        self.upcoming_task = TaskFactory(
            todo=self.todo, due_date=timezone.now() + timezone.timedelta(days=2)
        )
        self.overdue_task = TaskFactory(
            todo=self.todo, due_date=timezone.now() - timezone.timedelta(days=7)
        )
        self.completed_task = TaskFactory(
            todo=self.todo, is_completed=True, completed_at=timezone.now()
        )

    def test_tasks_list_returns_tasks_if_user_is_todo_owner(self):
        tasks = tasks_list(todo_id=self.todo.id, user=self.user)
        self.assertIn(self.upcoming_task, tasks)
        self.assertIn(self.overdue_task, tasks)

    def test_tasks_list_returns_empty_if_user_is_not_todo_owner(self):
        tasks = tasks_list(todo_id=self.todo.id, user=self.other_user)
        self.assertQuerySetEqual(tasks, [])

    def test_get_task_returns_task_if_found_and_user_is_todo_owner(self):
        task = get_task(task_id=self.upcoming_task.id, user=self.user)
        self.assertEqual(task.id, self.upcoming_task.id)

    def test_get_task_raises_error_if_task_not_found(self):
        with self.assertRaises(TodoAppBaseError):
            get_task(task_id=999, user=self.user)

    def test_get_tasks_stats_counts_tasks_by_category(self):
        stats = get_tasks_stats(user=self.user)

        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["overdue"], 1)
        self.assertEqual(stats["upcoming"], 1)
        self.assertEqual(stats["completed"], 1)

    def test_get_overdue_tasks_returns_user_overdue_tasks(self):
        overdue_tasks = get_overdue_tasks(user=self.user)

        self.assertEqual(len(overdue_tasks), 1)
        self.assertIn(self.overdue_task, overdue_tasks)

    def test_get_upcoming_tasks_this_week_returns_user_upcoming_tasks(self):
        upcoming_tasks = get_upcoming_tasks_this_week(user=self.user)

        self.assertEqual(len(upcoming_tasks), 1)
        self.assertIn(self.upcoming_task, upcoming_tasks)

    def test_get_completed_tasks_this_week_returns_user_completed_tasks(self):
        completed_tasks = get_completed_tasks_this_week(user=self.user)

        self.assertEqual(len(completed_tasks), 1)
        self.assertIn(self.completed_task, completed_tasks)

    def test_get_users_with_active_tasks_returns_users_with_non_completed_tasks(self):
        users = get_users_with_active_tasks()
        
        self.assertEqual(len(users), 1)
        self.assertIn(self.user, users)
        self.assertNotIn(self.other_user, users)