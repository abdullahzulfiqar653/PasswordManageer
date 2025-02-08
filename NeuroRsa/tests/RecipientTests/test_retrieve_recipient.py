from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from ..CustomClient import CustomTestClient


class RecipientRetrieveTests(APITestCase):
    
    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = CustomTestClient()
        
   
        self.url = "/api/recipients/"
        
        # Recipient data
        self.recipient_data = {
            "name": "Soha",
            "public_key": "MIIBIjANBgkqhkiG9w0BAQEFA...",
            "emoji": "🔒"
        }


    
    def test_get_recipient_by_id_success(self):

        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, self.recipient_data, format="json")
        recipient_id = response.data["id"]  

        get_url = f"{self.url}{recipient_id}/"
        response = self.client.get(get_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Soha")
        self.assertEqual(response.data["public_key"], "MIIBIjANBgkqhkiG9w0BAQEFA...")
        self.assertEqual(response.data["emoji"], "🔒")

    def test_get_recipient_by_id_not_found(self):
        get_url = f"{self.url}99999/"  
        response = self.client.get(get_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Not found.")



    def test_get_recipient_by_id_unauthorized(self):
        # Make GET request without authentication
        get_url = f"{self.url}1/"
        response = self.client.get(get_url, format="json")

        # Assert the response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")


    

    def test_get_recipient_by_id_invalid_format(self):
        # Make GET request with an invalid ID format
        get_url = f"{self.url}abc123/" 
        response = self.client.get(get_url, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Invalid ID format.")
