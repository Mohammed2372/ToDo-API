from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Todo
from django.urls import reverse  # Used to get URLs by name


# Test cases inherit from APITestCase
class TodoAPITests(APITestCase):
    def setUp(self):
        """
        This method runs *before* every single test.
        It's used to set up a clean environment.
        """

        # Create User 1
        self.user1 = User.objects.create_user(
            username="user1@test.com",
            email="user1@test.com",
            password="password123",
            first_name="User1",
        )

        # Create User 2
        self.user2 = User.objects.create_user(
            username="user2@test.com",
            email="user2@test.com",
            password="password123",
            first_name="User2",
        )

        # Create a task for User 1
        self.task1 = Todo.objects.create(owner=self.user1, title="User 1 Task")

        # Create a task for User 2
        self.task2 = Todo.objects.create(owner=self.user2, title="User 2 Task")

    # --- Authentication Tests ---

    def test_user_can_register(self):
        """
        Test that a new user can register.
        """
        url = "/register/"  # Or reverse('user-register')
        data = {
            "name": "NewUser",
            "email": "newuser@test.com",
            "password": "password123",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(response.data["name"], "NewUser")

    def test_user_cannot_register_with_existing_email(self):
        """
        Test that a user cannot register with an email (username) that already exists.
        """
        url = "/register/"
        data = {
            "name": "AnotherUser",
            "email": "user1@test.com",  # This email is already taken
            "password": "password123",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)  # No new user was created

    def test_user_can_login(self):
        """
        Test that a user can log in with correct email and password.
        """
        url = "/login/"  # Or reverse('token_obtain_pair')
        data = {"email": "user1@test.com", "password": "password123"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_cannot_login_with_wrong_password(self):
        """
        Test that login fails with an incorrect password.
        """
        url = "/login/"
        data = {"email": "user1@test.com", "password": "wrongpassword"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- Todo List/Create Tests (Security) ---

    def test_unauthenticated_user_cannot_list_todos(self):
        """
        Test that a user who is not logged in gets a 401 error.
        """
        # We do NOT call self.client.force_authenticate()
        url = "/todos/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_todo(self):
        """
        Test that a logged-in user can create a new todo.
        """
        self.client.force_authenticate(user=self.user1)
        url = "/todos/"
        data = {"title": "New Task", "description": "Test description"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 3)
        new_task = Todo.objects.get(title="New Task")
        self.assertEqual(new_task.owner, self.user1)

    def test_user_can_only_see_own_todos(self):
        """
        Test that a user cannot see tasks owned by other users.
        """
        self.client.force_authenticate(user=self.user1)
        url = "/todos/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check paginated response
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "User 1 Task")

    # --- Todo Detail (Retrieve, Update, Delete) Tests ---

    def test_user_can_retrieve_own_todo(self):
        """
        Test that a user can get the details of their own task.
        """
        self.client.force_authenticate(user=self.user1)
        url = f"/todos/{self.task1.id}/"  # e.g., /todos/1/

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.task1.title)

    def test_user_cannot_retrieve_other_users_todo(self):
        """
        Test security: A user cannot get the details of another user's task.
        """
        self.client.force_authenticate(user=self.user1)
        url = f"/todos/{self.task2.id}/"  # Task 2 belongs to User 2

        response = self.client.get(url)

        # Should return 404 Not Found, as if the task doesn't exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_todo(self):
        """
        Test that a user can update their own task.
        """
        self.client.force_authenticate(user=self.user1)
        url = f"/todos/{self.task1.id}/"
        data = {"title": "UPDATED Task Title", "description": "Updated desc."}

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "UPDATED Task Title")

        # Verify the change in the database
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, "UPDATED Task Title")

    def test_user_cannot_update_other_users_todo(self):
        """
        Test security: A user cannot update another user's task.
        """
        self.client.force_authenticate(user=self.user1)
        url = f"/todos/{self.task2.id}/"  # Task 2 belongs to User 2
        data = {"title": "I am hacking you"}

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_delete_own_todo(self):
        """
        Test that a user can delete their own task.
        """
        self.client.force_authenticate(user=self.user1)
        url = f"/todos/{self.task1.id}/"

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Todo.objects.filter(id=self.task1.id).exists())

    def test_user_cannot_delete_other_users_todo(self):
        """
        Test security: A user cannot delete another user's task.
        """
        self.client.force_authenticate(user=self.user1)
        url = f"/todos/{self.task2.id}/"  # Task 2 belongs to User 2

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Todo.objects.filter(id=self.task2.id).exists())

    # --- Toggle Complete Test ---

    def test_user_can_toggle_complete_own_todo(self):
        """
        Test that a user can toggle their task's 'completed' status.
        """
        self.client.force_authenticate(user=self.user1)
        url = f"/todos/{self.task1.id}/complete/"

        # Check it's False to begin with
        self.assertFalse(self.task1.completed)

        # First toggle: should become True
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["completed"], True)

        # Check in the database
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.completed)

        # Second toggle: should become False
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["completed"], False)

        self.task1.refresh_from_db()
        self.assertFalse(self.task1.completed)

    def test_user_cannot_toggle_other_users_todo(self):
        """
        Test security: A user cannot toggle another user's task.
        """
        self.client.force_authenticate(user=self.user1)
        url = f"/todos/{self.task2.id}/complete/"  # Task 2 belongs to User 2

        response = self.client.put(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
