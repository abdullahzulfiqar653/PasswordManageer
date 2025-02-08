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

        response = self.client.post(self.url, self.recipient_data, format="json")
        print(response.data)
        self.recipient_id = response.data["id"]


    def test_update_recipient_success(self):
        
        update_url = f"{self.url}{self.recipient_id}/"
        response = self.client.put(update_url, self.updated_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Bobby")
        self.assertEqual(response.data["emoji"], "🔐")



    def test_update_recipient_not_found(self):
        self.client.force_authenticate(self.user)
        update_url = f"{self.url}nonexistent-id/"
        response = self.client.put(update_url, self.updated_data, format="json")
    
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)
        self.assertEqual(str(response.data["detail"]), "No Recipient matches the given query.")



    def test_update_recipient_unauthorized(self):
        self.client.logout() 
        update_url = f"{self.url}{self.recipient_id}/"
        response = self.client.put(update_url, self.updated_data, format="json")
        
        # Assert unauthorized error
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_update_recipient_invalid_data(self):
        self.client.force_authenticate(self.user)
      
        invalid_data = {
            "name": "Bobby",
            "emoji": "🔐"
        }
        update_url = f"{self.url}{self.recipient_id}/"
        response = self.client.put(update_url, invalid_data, format="json")
        
        # Assert bad request error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("public_key", response.data)

