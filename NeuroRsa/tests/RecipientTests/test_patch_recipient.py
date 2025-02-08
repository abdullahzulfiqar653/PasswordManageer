from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..CustomClient import CustomTestClient


class RecipientTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = CustomTestClient()

        self.url = "/api/recipients/"

        self.recipient_data = {
            "name": "Soha",
            "public_key": "MIIBIjANBgkqhkiG9w0BAQEFA...",
            "emoji": "🔒"
        }

        self.updated_data = {
            "name": "Bobby",
            "public_key": "MIIBIjANBgkqhkiG9w0BAQEFA...",
            "emoji": "🔐"
        }

        self.client.force_authenticate(self.user)

        # Create a recipient
        response = self.client.post(self.url, self.recipient_data, format="json")
        self.recipient_id = response.data["id"]

    def test_patch_recipient_success(self):
        patch_url = f"{self.url}{self.recipient_id}/"
        partial_data = {
            "emoji": "🔑"  
        }

        response = self.client.patch(patch_url, partial_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["emoji"], "🔑")
        self.assertEqual(response.data["name"], "Soha")  
    def test_patch_recipient_not_found(self):
        patch_url = f"{self.url}nonexistent-id/"
        partial_data = {
            "emoji": "🔑"
        }

        response = self.client.patch(patch_url, partial_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)
        self.assertEqual(str(response.data["detail"]), "No Recipient matches the given query.")

    def test_patch_recipient_unauthorized(self):
        self.client.logout()
        patch_url = f"{self.url}{self.recipient_id}/"
        partial_data = {
            "emoji": "🔑"
        }

        response = self.client.patch(patch_url, partial_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

