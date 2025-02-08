from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from ..CustomClient import CustomTestClient

    
class KeyPairUpdateTests(APITestCase):
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

        # Create a keypair to update later
        response = self.client.post(self.url, self.keypair_data, format="json")
        self.keypair_id = response.data["id"]

    def test_update_keypair(self):
        updated_data = {
            "name": "Updated KeyPair",
            "email": "updateduser@example.com",
            "passphrase": "newSecurePassphrase123"  
        }

        response = self.client.put(f"{self.url}{self.keypair_id}", updated_data, format="json")

        self.assertEqual(response.status_code, 200)

        # Check if the response contains the updated data
        self.assertEqual(response.data["id"], self.keypair_id)
        self.assertEqual(response.data["name"], updated_data["name"])
        self.assertEqual(response.data["email"], updated_data["email"])
        self.assertNotIn("passphrase", response.data)  
        self.assertIn("public_key", response.data)  
        self.assertIn("private_key", response.data)  


    def test_update_keypair_not_found(self):

        invalid_keypair_id = 99999
        updated_data = {
            "name": "Non-Existent KeyPair",
            "email": "nonexistent@example.com",
            "passphrase": "somePassphrase"
        }
        
        response = self.client.put(f"{self.url}{invalid_keypair_id}/", updated_data, format="json")
        self.assertEqual(response.status_code, 404)


    def test_update_keypair_invalid_data(self):
    
        invalid_data = {
            "email": "updateduser@example.com",
            "passphrase": "newSecurePassphrase123"
        }

        response = self.client.put(f"{self.url}{self.keypair_id}", invalid_data, format="json")
        self.assertEqual(response.status_code, 200)


    def test_update_keypair_invalid_email(self):
        # Test with invalid email format
        invalid_data = {
            "name": "Updated KeyPair",
            "email": "invalidemailformat",  # Invalid email
            "passphrase": "newSecurePassphrase123"
        }

        response = self.client.put(f"{self.url}{self.keypair_id}", invalid_data, format="json")
        # Assert that the response status code is 400 (bad request)
        self.assertEqual(response.status_code, 400)

        # Assert that the response contains error about invalid email
        self.assertIn("email", response.data)

    


