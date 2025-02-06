import logging
from rest_framework import status
from rest_framework.test import APITestCase
from PasswordManager.models.folder import Folder
from django.contrib.auth.models import User
from django.conf import settings


def get_base_url():
    # Use the domain specified for PasswordManager in your settings
    base_url = f"http://{settings.ACTIVE_HOSTS['PasswordManager']}:8000/api"
    return base_url


class TestFolderListCreateView(APITestCase):
    def setUp(self) -> None:
        """Reduce the log level to avoid errors like 'not found'"""
        logger = logging.getLogger("django.request")
        self.previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

        self.user = User.objects.create_user(username="user", password="password")
        self.outsider = User.objects.create_user(
            username="outsider", password="password"
        )

        self.folder1 = Folder.objects.create(user=self.user, title="Folder 1")
        self.folder2 = Folder.objects.create(user=self.user, title="Folder 2")

        return super().setUp()

    def test_user_list_folders(self):
        url = f"{get_base_url()}/folders/"  # Use the correct base URL
        self.client.force_authenticate(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        folder_titles = [folder["title"] for folder in response.json()]
        self.assertCountEqual(folder_titles, ["Folder 1", "Folder 2"])

    def test_outsider_list_folders(self):
        url = f"{get_base_url()}/folders/"  # Use the correct base URL
        self.client.force_authenticate(self.outsider)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_folder(self):
        url = f"{get_base_url()}/folders/"  # Use the correct base URL
        self.client.force_authenticate(self.user)
        data = {"title": "New Folder"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        folder = Folder.objects.get(id=response.json()["id"])
        self.assertEqual(folder.title, "New Folder")
        self.assertEqual(folder.user, self.user)

    def test_outsider_create_folder(self):
        url = f"{get_base_url()}/folders/"  # Use the correct base URL
        self.client.force_authenticate(self.outsider)
        data = {"title": "Outsider Folder"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
