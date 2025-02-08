from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from ..CustomClient import CustomTestClient


class RecipientTests(APITestCase):
    

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = CustomTestClient()
       
        self.url = "/api/recipients/"
        self.data = {
            "name": "Alice",
            "public_key": "MIIBIjANBgkqhkiG9w0BAQEFA...",
            "emoji": "🔒"
        }
    

    def test_create_recipient_success(self):
        self.client.force_authenticate(self.user)
       
        
        response = self.client.post(self.url, self.data, format="json")


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn("id", response.data)
        self.assertEqual(response.data["name"], "Alice")
        self.assertEqual(response.data["public_key"], "MIIBIjANBgkqhkiG9w0BAQEFA...")
        self.assertEqual(response.data["emoji"], "🔒")

    def test_fail_missing_data(self):
        self.client.force_authenticate(self.user)   
        data = {}  
        
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)  
        self.assertIn("public_key", response.data)  

    def test_fail_unauthorized_user(self):
       
        response = self.client.post(self.url, self.data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_fail_duplicate_name(self):
        self.client.force_authenticate(self.user)
        self.client.post(self.url, self.data, format="json")


        duplicate_data = {
            "name": "Alice",  
            "public_key": "MIIBIjANBgkqhkiG9w0BAQEFA...",
            "emoji": "🔐"
        }
        
        response = self.client.post(self.url, duplicate_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(str(response.data["non_field_errors"][0]), "Recipient with this name already exists")

    def test_create_recipient_missing_emoji(self):
        self.client.force_authenticate(self.user)
        data = {
            "name": "Alice",
            "public_key": "M..."
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["name"], "Alice")
        self.assertIn("emoji", response.data)
        self.assertIsNone(response.data["emoji"])  