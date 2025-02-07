from rest_framework import status
from rest_framework.test import APITestCase
from PasswordManager.models.password import Password
from django.contrib.auth.models import User
from PasswordManager.models.folder import Folder
from rest_framework.test import APIClient


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
    
    def patch(self, path, data=None, **extra):
        if "HTTP_HOST" not in extra:
            extra["HTTP_HOST"] = "pm:8000"
        return super().patch(path, data, **extra)

    def delete(self, path, **extra):
        if "HTTP_HOST" not in extra:
            extra["HTTP_HOST"] = "pm:8000"
        return super().delete(path, **extra)


class PasswordUPatchViewTest(APITestCase):
    
    def setUp(self):
        # Create users for testing
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.user1 = User.objects.create_user(username="testuser1", password="testpassword")

        self.folder = Folder.objects.create(user=self.user, title="Test Folder")
        self.client.login(username="testuser", password="testpassword")
      
        # Create a password entry for the user
        self.password = Password.objects.create(
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
        self.client = CustomTestClient()

    def test_patch_password_success(self):

        patch_data = {
            "title": "Partially Updated Test Password"
        }
        
        self.client.force_authenticate(self.user)
        response = self.client.patch(self.url, patch_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Partially Updated Test Password")
        self.assertEqual(response.data["url"], "http://password.com")  

    def test_patch_password_forbidden(self):
        patch_data = {
            "title": "Unauthorized User Update"
        }

        # Authenticate as a different user
        self.client.force_authenticate(self.user1)
        response = self.client.patch(self.url, patch_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_password_invalid_data(self):
        patch_data = {
            "title": ""  # Title should not be empty based on model constraints
        }

        self.client.force_authenticate(self.user)
        response = self.client.patch(self.url, patch_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)  


 