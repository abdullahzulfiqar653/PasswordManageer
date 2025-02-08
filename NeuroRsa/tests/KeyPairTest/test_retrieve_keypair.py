from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..CustomClient import CustomTestClient


class KeyPairRetrieveTests(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = CustomTestClient()  
      
        self.client.force_authenticate(self.user)
        
        self.url = "/api/keypairs/"

        self.keypair_data = {
            "name": "Test KeyPair",
            "email": "testuser@example.com",
            "passphrase": "securePassphrase123"
        }

        response = self.client.post(self.url, self.keypair_data, format="json")
        self.keypair_id = response.data["id"] 


    def test_retrieve_keypair(self):
         
        response = self.client.get(f"{self.url}{self.keypair_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.keypair_id)
        self.assertEqual(response.data["name"], self.keypair_data["name"])
        self.assertEqual(response.data["email"], self.keypair_data["email"])
        self.assertNotIn("passphrase", response.data)
        self.assertIn("public_key", response.data)
        self.assertIn("private_key", response.data)



    def test_retrieve_keypair_not_exist(self):

        invalid_keypair_id = 99999
        response = self.client.get(f"{self.url}{invalid_keypair_id}/")
        self.assertEqual(response.status_code, 404)


    def test_retrieve_keypair_other_user(self):
        other_user = User.objects.create_user(username="otheruser", password="password123")
        self.client.force_authenticate(other_user)

        other_keypair_data = {
            "name": "Other User KeyPair",
            "email": "otheruser@example.com",
            "passphrase": "otherPassphrase123"
        }
        response = self.client.post(self.url, other_keypair_data, format="json")
        other_keypair_id = response.data["id"]
        
        response = self.client.get(f"{self.url}{other_keypair_id}/")
        self.assertEqual(response.status_code, 404)



