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
            "name": "Alice",
            "public_key": "MIIBIjANBgkqhkiG9w0BAQEFA...",
            "emoji": "🔒"
        }

        self.client.force_authenticate(self.user)

        # Create a recipient
        response = self.client.post(self.url, self.recipient_data, format="json")
        self.recipient_id = response.data["id"]

    def test_delete_recipient_success(self):
        delete_url = f"{self.url}{self.recipient_id}/"
        response = self.client.delete(delete_url)

        # Assert that the recipient is deleted
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Ensure the recipient no longer exists
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_recipient_not_found(self):
        delete_url = f"{self.url}nonexistent-id/"
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)
        self.assertEqual(str(response.data["detail"]), "No Recipient matches the given query.")

    def test_delete_recipient_unauthorized(self):
        self.client.logout()
        delete_url = f"{self.url}{self.recipient_id}/"
        response = self.client.delete(delete_url)

        # Assert unauthorized error
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

