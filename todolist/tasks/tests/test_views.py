from rest_framework.test import APITestCase
from todolist.todos.tests.factories import UserFactory, TodoListFactory
from todolist.tasks.tests.factories import TaskFactory
from django.urls import reverse

from rest_framework import status
# Create your tests here.


class TaskListViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.todo = TodoListFactory(owner=self.user)

        self.task_1 = TaskFactory(
            todo=self.todo, due_date="2026-06-07T00:00:00Z", is_completed=True
        )
        self.task_2 = TaskFactory(
            todo=self.todo, due_date="2026-06-10T00:00:00Z", is_completed=False
        )

        self.other_todo = TodoListFactory()
        self.other_task = TaskFactory()

        self.client.force_authenticate(user=self.user)

    def test_task_list_returns_200(self):
        response = self.client.get(reverse("task-list", args=[self.todo.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_task_list_returns_only_own_tasks(self):
        response = self.client.get(reverse("task-list", args=[self.todo.id]))

        tasks = response.data["results"]
        ids = [task["id"] for task in tasks]

        self.assertIn(self.task_1.id, ids)

        self.assertNotIn(self.other_task.id, ids)

    def test_task_list_returns_403_for_non_task_owner(self):
        response = self.client.get(reverse("task-list", args=[self.other_todo.id]))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_task_list_filters_by_is_completed(self):
        response = self.client.get(
            reverse("task-list", args=[self.todo.id]), {"is_completed": "true"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        tasks = response.data["results"]

        self.assertEqual(len(tasks), 1)
        self.assertTrue(all(task["is_completed"] for task in tasks))

    def test_task_list_filters_by_due_date(self):
        response = self.client.get(
            reverse("task-list", args=[self.todo.id]),
            {"due_date_after": "2026-06-08", "due_date_before": "2026-06-10"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        tasks = response.data["results"]
        
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["due_date"],"2026-06-10T00:00:00Z")


class TaskDetailViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.todo = TodoListFactory(owner=self.user)

        self.task = TaskFactory(todo=self.todo)

        self.other_task = TaskFactory()

        self.client.force_authenticate(user=self.user)

    def test_task_detail_returns_200(self):
        response = self.client.get(reverse("task-detail", args=[self.task.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_task_detail_returns_only_own_task(self):
        response = self.client.get(reverse("task-detail", args=[self.task.id]))

        task = response.data

        self.assertEqual(self.task.id, task["id"])
        self.assertFalse(self.other_task.id == task["id"])

    def test_task_detail_returns_403_for_non_task_owner(self):
        response = self.client.get(reverse("task-detail", args=[self.other_task.id]))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TaskCreateViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.todo = TodoListFactory(owner=self.user)

        self.task = TaskFactory(todo=self.todo)

        self.other_todo = TodoListFactory()

        self.client.force_authenticate(user=self.user)

    def test_task_create_returns_201(self):
        response = self.client.post(
            reverse("task-create", args=[self.todo.id]), data={"name": "test"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_task_create_returns_task(self):
        response = self.client.post(
            reverse("task-create", args=[self.todo.id]), data={"name": "test"}
        )
        task = response.data

        self.assertEqual(task["name"], "test")

    def test_task_create_returns_403_for_non_own_todo(self):
        response = self.client.post(
            reverse("task-create", args=[self.other_todo.id]), data={"name": "test"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TaskUpdateViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.todo = TodoListFactory(owner=self.user)

        self.task = TaskFactory(todo=self.todo)

        self.other_todo = TodoListFactory()
        self.other_task = TaskFactory(todo=self.other_todo)

        self.client.force_authenticate(user=self.user)

    def test_task_update_returns_200(self):
        response = self.client.patch(
            reverse("task-update", args=[self.task.id]), data={"name": "updated field"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_task_update_returns_task(self):
        response = self.client.patch(
            reverse("task-update", args=[self.task.id]), data={"name": "updated field"}
        )

        task = response.data
        self.assertEqual(task["name"], "updated field")

    def test_task_update_returns_403_for_non_own_task(self):
        response = self.client.patch(
            reverse("task-update", args=[self.other_task.id]),
            data={"name": "updated field"},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TaskDeleteViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.todo = TodoListFactory(owner=self.user)

        self.task = TaskFactory(todo=self.todo)

        self.other_todo = TodoListFactory()
        self.other_task = TaskFactory(todo=self.other_todo)

        self.client.force_authenticate(user=self.user)

    def test_task_delete_returns_204(self):
        response = self.client.delete(reverse("task-delete", args=[self.task.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_task_delete_returns_403_for_non_own_task(self):
        response = self.client.delete(reverse("task-delete", args=[self.other_task.id]))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
