from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from ..CustomClient import CustomTestClient


class RecipientTests(APITestCase):
    
    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = CustomTestClient()
        
        # URL for listing recipients
        self.url = "/api/recipients/"
        
        # Recipient data
        self.recipient_data_1 = {
            "name": "Soha",
            "public_key": "MIIBIjANBgkqhkiG9w0BAQEFA...",
            "emoji": "🔒"
        }
        
        self.recipient_data_2 = {
            "name": "Alice",
            "public_key": "MIIBIjANBgkqhkiG9w0BAQEFA...",
            "emoji": "🔐"
        }
    
    def test_list_all_recipients(self):
        # Create recipients
        self.client.force_authenticate(self.user)
        self.client.post(self.url, self.recipient_data_1, format="json")
        self.client.post(self.url, self.recipient_data_2, format="json")

        # Make GET request to fetch all recipients
        response = self.client.get(self.url, format="json")

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 2 recipients
        self.assertEqual(response.data[0]["name"], "Soha")
        self.assertEqual(response.data[1]["name"], "Alice")
        self.assertIn("public_key", response.data[0])
        self.assertIn("emoji", response.data[1])

    def test_list_all_recipients_unauthorized(self):
        response = self.client.get(self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

