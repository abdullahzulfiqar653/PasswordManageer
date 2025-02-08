from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..CustomClient import CustomTestClient


class KeyPairPatchTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = CustomTestClient()  # Use the custom test client if necessary
        self.client.force_authenticate(self.user)

        self.url = "/api/keypairs/"
        self.keypair_data = {
            "name": "Test KeyPair",
            "email": "testuser@example.com",
            "passphrase": "securePassphrase123"
        }

        response = self.client.post(self.url, self.keypair_data, format="json")
        self.keypair_id = response.data["id"]

    def test_patch_keypair(self):
        # Only updating the email
        patch_data = {
            "email": "updateduser@example.com"  
        }

        response = self.client.patch(f"{self.url}{self.keypair_id}", patch_data, format="json")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], "updateduser@example.com")
        # Ensure other fields are not affected
        self.assertEqual(response.data["name"], self.keypair_data["name"])



    
    def test_patch_keypair_non_existent(self):
        # Test PATCH request with a non-existent keypair ID (404)
        invalid_keypair_id = 99999
        patch_data = {
            "email": "updateduser@example.com"
        }

        response = self.client.patch(f"{self.url}{invalid_keypair_id}", patch_data, format="json")
        
        self.assertEqual(response.status_code, 404)
    

    def test_patch_keypair_invalid_email(self):
        # Test with an invalid email format
        invalid_patch_data = {
            "email": "invalidemail.com",  
        }

        response = self.client.patch(f"{self.url}{self.keypair_id}", invalid_patch_data, format="json")
    
        self.assertEqual(response.status_code, 400)

        self.assertIn("email", response.data)