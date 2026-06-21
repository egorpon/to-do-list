from django.test import TestCase
from rest_framework.test import APITestCase
from todolist.tasks.tests.factories import TaskFactory
from todolist.todos.tests.factories import TodoListFactory, UserFactory
from django.urls import reverse
from rest_framework import status
# Create your tests here.


class TodoListViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.todo = TodoListFactory(owner=self.user)
        self.task = TaskFactory(todo=self.todo)

        self.todo2 = TodoListFactory(owner=self.user)
        self.task2 = TaskFactory(todo=self.todo2)

 

    def test_authenticated_user_can_retrieve_lists(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        todos = response.json()

        self.assertTrue(all(todo["owner"] == self.user.id for todo in todos["results"]))

    def test_todo_list_view_unauthenticated(self):
        response = self.client.get(reverse("list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
