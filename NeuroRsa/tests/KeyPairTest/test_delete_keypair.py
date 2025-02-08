from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..CustomClient import CustomTestClient



class KeyPairDeleteTests(APITestCase):

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



    def test_delete_keypair(self):
        response = self.client.delete(f"{self.url}{self.keypair_id}")
        self.assertEqual(response.status_code, 204)
        response = self.client.get(f"{self.url}{self.keypair_id}/")
        self.assertEqual(response.status_code, 404)


    def test_delete_keypair_not_exist(self):

        invalid_keypair_id = 99999  
        response = self.client.delete(f"{self.url}{invalid_keypair_id}/")

        self.assertEqual(response.status_code, 404)
