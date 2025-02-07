from rest_framework import status
from rest_framework.test import APITestCase
from PasswordManager.models.password import Password
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from PasswordManager.models.folder import Folder





class CustomTestClient(APIClient):
    def get(self, path, **extra):
        if "HTTP_HOST" not in extra:
            extra["HTTP_HOST"] = "pm:8000"
        return super().get(path, **extra)

    def post(self, path, data=None, **extra):
        if "HTTP_HOST" not in extra:
            extra["HTTP_HOST"] = "pm:8000"
        return super().post(path, data, **extra)

    def put(self, path, data=None, **extra):
        if "HTTP_HOST" not in extra:
            extra["HTTP_HOST"] = "pm:8000"
        return super().put(path, data, **extra)

    def delete(self, path, **extra):
        if "HTTP_HOST" not in extra:
            extra["HTTP_HOST"] = "pm:8000"
        return super().delete(path, **extra)


class PasswordRetrieveViewTest(APITestCase):
    
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.folder = Folder.objects.create(user=self.user, title="Test Folder")
        self.client.login(username="testuser", password="testpassword")
        self.user1 = User.objects.create_user(username="testuser1", password="testpassword1")
        

        self.password =  Password.objects.create(
            url="http://password.com",
            notes="Old password notes",
            title="Test Password",
            emoji="🔑",
            folder=self.folder,
            username="testuser",
            password="testpassword",
            user=self.user
        )

        self.url = f"/api/passwords/{self.password.id}/"
        self.client=CustomTestClient()


    def test_retrieve_password_success(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Password")
        self.assertEqual(response.data["username"], "testuser")



    def test_retrieve_password_failure(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_create_password_without_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")
        