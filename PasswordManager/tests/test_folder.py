import logging
from django.conf import settings
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
        response = self.client.get(self.url)
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
