from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..CustomClient import CustomTestClient

class KeyPairListTests(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = CustomTestClient()
        self.client.force_authenticate(self.user)
        self.url = "/api/keypairs/"

        # Create a couple of key pairs for testing
        self.keypair_data_1 = {
            "name": "KeyPair 1",
            "email": "user1@example.com",
            "passphrase": "securePassphrase123"
        }
        self.keypair_data_2 = {
            "name": "KeyPair 2",
            "email": "user2@example.com",
            "passphrase": "anotherPassphrase456"
        }
        
   
        self.client.post(self.url, self.keypair_data_1, format="json")
        self.client.post(self.url, self.keypair_data_2, format="json")


    def test_get_keypair_list(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        # Assert that the list contains the key pairs created
        self.assertEqual(len(response.data['results']), 2)  
        self.assertEqual(response.data['results'][0]['name'], self.keypair_data_1['name'])
        self.assertEqual(response.data['results'][1]['name'], self.keypair_data_2['name'])


    def test_get_keypair_list_unauthenticated(self):
        other_user = User.objects.create_user(username="otheruser", password="password123")
        self.client.force_authenticate(other_user)

        response = self.client.get(self.url)
        
        # Assert the response status code is 401 Unauthorized
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")
