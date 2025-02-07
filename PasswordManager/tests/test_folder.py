import logging
from rest_framework import status
from rest_framework.test import APITestCase
from PasswordManager.models.folder import Folder
from django.contrib.auth.models import User
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

    def delete(self, path, **extra):
        if "HTTP_HOST" not in extra:
            extra["HTTP_HOST"] = "pm:8000"
        return super().delete(path, **extra)



class BaseFolderTest(APITestCase):
    """Base test class for folder tests that sets up common objects"""

    def setUp(self) -> None:
        """Set up users and folders for the test"""
        self.user = User.objects.create_user(username="user", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")
        self.folder1 = Folder.objects.create(user=self.user, title="Folder 1")
        self.folder2 = Folder.objects.create(user=self.user2, title="Folder 2")
        self.client = CustomTestClient()
        

class TestFolderListCreateView(APITestCase):
    def setUp(self) -> None:
        """Reduce the log level to avoid errors like 'not found'"""
        logger = logging.getLogger("django.request")
        self.previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

        self.user = User.objects.create_user(username="user", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")

        self.folder1 = Folder.objects.create(user=self.user, title="Folder 1")
        self.folder2 = Folder.objects.create(user=self.user, title="Folder 2")
        self.client = CustomTestClient()
        self.url = "/api/folders/"
        # return super().setUp()

    def test_user_list_folders(self):
        self.client.force_authenticate(self.user)
        response = self.client.get('/api/folders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        folder_titles = [folder["title"] for folder in response.json()["results"]]
        self.assertCountEqual(folder_titles, ["Folder 1", "Folder 2"])

    def test_user2_list_folders(self):
        self.client.force_authenticate(self.user2)
        response = self.client.get(self.url)
        self.assertCountEqual(response.json()["results"], [])

    def test_create_folder(self):
        self.client.force_authenticate(self.user)
        data = {"title": "New Folder"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        folder = Folder.objects.get(id=response.json()["id"])
        self.assertEqual(folder.title, "New Folder")
        self.assertEqual(folder.user, self.user)



class FolderRetrieveViewTest(BaseFolderTest):
    def test_retrieve_folder_success(self):
        """Test retrieving a folder by its owner"""
        self.client.force_authenticate(self.user)
        response = self.client.get(f'/api/folders/{self.folder1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.folder1.id)
        self.assertEqual(response.data['title'], 'Folder 1')

    
    def test_retrieve_folder_not_found(self):
        """Test retrieving a folder that does not belong to the authenticated user"""
        self.client.force_authenticate(self.user)  # Authenticating as user1
        response = self.client.get(f'/api/folders/{self.folder2.id}/')  # Trying to access folder2, owned by user2
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'No Folder matches the given query.')


class FolderUpdateViewTest(BaseFolderTest):

    def test_update_folder_success(self):
        """Test updating a folder by its owner"""
        self.client.force_authenticate(self.user)
        data = {'title': 'Updated Folder Title'}
        response = self.client.put(f'/api/folders/{self.folder1.id}/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Folder Title')

        # Verify the folder is updated in the database
        self.folder1.refresh_from_db()
        self.assertEqual(self.folder1.title, 'Updated Folder Title')
    

    def test_update_folder_not_found(self):
        """Test deleting a folder that does not belong to the authenticated user"""
        self.client.force_authenticate(self.user)  # Authenticating as user1
        response = self.client.delete(f'/api/folders/{self.folder2.id}/')  # Trying to delete folder2, owned by user2
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'No Folder matches the given query.')


class FolderDeleteViewTest(BaseFolderTest):

    def test_delete_folder_success(self):

        """Test deleting a folder by its owner"""
        self.client.force_authenticate(self.user)
        response = self.client.delete(f'/api/folders/{self.folder1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Folder.objects.filter(id=self.folder1.id).exists())



    def test_delete_folder_not_found(self):
        """Test deleting a folder that does not belong to the authenticated user"""
        self.client.force_authenticate(self.user)  # Authenticating as user1
        response = self.client.delete(f'/api/folders/{self.folder2.id}/')  # Trying to delete folder2, owned by user2
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'No Folder matches the given query.')
