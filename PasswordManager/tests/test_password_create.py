from rest_framework import status
from PasswordManager.models.password import Password
from PasswordManager.models.folder import Folder
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from .customclient import CustomTestClient



class BaseFolderTest(APITestCase):
    """Base test class for folder tests that sets up common objects"""

    def setUp(self) -> None:

        self.user = User.objects.create_user(username="user", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")
        self.folder1 = Folder.objects.create(user=self.user, title="Folder 1")
        self.folder2 = Folder.objects.create(user=self.user2, title="Folder 2")
        self.client = CustomTestClient()
        self.url = '/api/passwords/'  

        self.folder = self.folder1  

        self.data = {
            "url": "http://example.com",
            "notes": "Sample password notes",
            "title": "Test Password",
            "emoji": "🔒",
            "folder": self.folder.id,
            "username": "user123",
            "password": "secret123",
        }
        self.client.force_authenticate(self.user)

class TestCasePasswordSerializer(BaseFolderTest):
    
    def test_create_password_entry(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        password_entry = Password.objects.get(id=response.data['id'])

        self.assertEqual(password_entry.title, self.data['title'])
        self.assertEqual(password_entry.username, self.data['username'])
        self.assertEqual(password_entry.folder.id, self.data['folder'])



    def test_folder_not_belonging_to_user(self):
        self.data['folder'] = self.folder2.id
        response = self.client.post(self.url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('folder', response.data)  

    def test_duplicate_title(self):
     
        Password.objects.create(
            url="http://oldpassword.com",
            notes="Old password notes",
            title="Test Password",
            emoji="🔑",
            folder=self.folder,
            username="olduser",
            password="oldpassword123",
            user=self.user
        )

        response = self.client.post(self.url, self.data, format='json')

        # Assert that the status code is 400 Bad Request due to the duplicate title
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data) 

    
    def test_create_password_with_file(self):
    
        from io import BytesIO
        from django.core.files.uploadedfile import InMemoryUploadedFile

        file_data = BytesIO(b"Sample file content")
        file = InMemoryUploadedFile(file_data, None, "testfile.txt", "text/plain", len(file_data.getvalue()), None)
        self.data['file'] = file

     
        response = self.client.post(self.url, self.data, format='multipart')  

        if response.status_code != status.HTTP_201_CREATED:
            print("Response data:", response.data)


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        password_entry = Password.objects.get(id=response.data['id'])
        self.assertIsNotNone(password_entry.file)
        self.assertEqual(password_entry.content_type, 'text/plain')


    def test_create_password_without_folder(self):

        del self.data['folder']
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('folder', response.data)  

