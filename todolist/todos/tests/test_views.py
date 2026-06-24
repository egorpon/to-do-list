from rest_framework.test import APITestCase, APIClient
from todolist.tasks.tests.factories import TaskFactory
from todolist.todos.tests.factories import TodoListFactory, UserFactory
from django.urls import reverse
from rest_framework import status
# Create your tests here.


class TodoListViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.todo = TodoListFactory(name="test", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_todo_list_returns_200(self):
        response = self.client.get(reverse("todo-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_todo_list_returns_only_own_todos(self):
        other_todo = TodoListFactory()

        response = self.client.get(reverse("todo-list"))
        todos = response.data

        ids = [todo["id"] for todo in todos["results"]]

        self.assertIn(self.todo.id, ids)

        self.assertNotIn(other_todo.id, ids)


class TodoDetailViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.todo = TodoListFactory(name="test", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_todo_detail_returns_200(self):
        response = self.client.get(reverse("todo-detail", args=[self.todo.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_todo_detail_returns_only_own_todo(self):

        response = self.client.get(reverse("todo-detail", args=[self.todo.id]))

        todo = response.data

        self.assertEqual(self.todo.name, todo["name"])

    def test_todo_detail_returns_403_for_non_owner(self):
        other_todo = TodoListFactory()

        response = self.client.get(reverse("todo-detail", args=[other_todo.id]))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TodoCreateViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()

        self.client.force_authenticate(user=self.user)

    def test_todo_create_returns_201(self):
        response = self.client.post(reverse("todo-create"), data={"name": "test"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_todo_create_returns_todo(self):
        response = self.client.post(reverse("todo-create"), data={"name": "test"})
        todo = response.data
        self.assertEqual(todo["name"], "test")


class TodoUpdateViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.todo = TodoListFactory(owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_todo_update_returns_200(self):
        response = self.client.patch(
            reverse("todo-update", args=[self.todo.id]), data={"name": "updated field"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_todo_update_returns_403_for_non_owner(self):
        other_todo = TodoListFactory()
        response = self.client.patch(
            reverse("todo-update", args=[other_todo.id]), data={"name": "updated field"}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_todo_update_returns_todo(self):
        response = self.client.patch(
            reverse("todo-update", args=[self.todo.id]), data={"name": "updated field"}
        )
        todo = response.data
        self.assertEqual(todo["name"], "updated field")


class TodoDeleteViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.todo = TodoListFactory(owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_todo_delete_returns_204(self):
        response = self.client.delete(reverse("todo-delete", args=[self.todo.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_todo_delete_returns_403_for_non_owner(self):
        other_todo = TodoListFactory()
        response = self.client.delete(reverse("todo-delete", args=[other_todo.id]))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
