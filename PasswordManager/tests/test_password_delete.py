from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from PasswordManager.models.password import Password
from PasswordManager.models.folder import Folder
from .customclient import CustomTestClient


class TestDeletePassword(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.folder = Folder.objects.create(title="Default Folder", user=self.user)

        self.password1 = Password.objects.create(
            user=self.user,
            title="Password 1",
            notes="Test password 1",  
            folder=self.folder
        )
        self.password2 = Password.objects.create(
            user=self.user,
            title="Password 2",
            notes="Test password 2",  
            folder=self.folder
        )

        self.other_user = User.objects.create_user(username="otheruser", password="otherpassword")

        self.client = CustomTestClient()

        self.password_delete_url = "/api/passwords/{}/"  

    def test_delete_password_authenticated_user(self):
    
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.password_delete_url.format(self.password1.id))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  
        self.assertFalse(Password.objects.filter(id=self.password1.id).exists())
        self.assertTrue(Password.objects.filter(id=self.password2.id).exists())

    def test_delete_password_unauthenticated_user(self):

        response = self.client.delete(self.password_delete_url.format(self.password1.id))  
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  

    def test_delete_password_other_user(self):

        self.client.force_authenticate(self.other_user)
        response = self.client.delete(self.password_delete_url.format(self.password1.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  
    



