from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from NeuroRsa.models.keypair import KeyPair
from ..CustomClient import CustomTestClient



class KeyPairTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.client = CustomTestClient()
        self.url = "/api/keypairs/"



    def test_create_keypair(self):
        self.client.force_authenticate(self.user)
        data = {
            "name": "test_keypair",
            "email": "testuser@example.com",
            "passphrase": "secretpassphrase"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(KeyPair.objects.count(), 1)
        self.assertEqual(KeyPair.objects.get().name, "test_keypair")



    def test_create_keypair_without_passkey(self):
        self.client.force_authenticate(self.user)
        data = {
            "name": "test_keypair",
            "email": "testuser@example.com"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(KeyPair.objects.count(), 1)
        self.assertEqual(KeyPair.objects.get().name, "test_keypair")



    def test_create_keypair_unauthorized(self):
        data = {
            "name": "test_keypair",
            "email": "testuser@example.com"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



    def test_create_keypair_invalid_email(self):
        self.client.force_authenticate(self.user)
        data = {
            "name": "test_keypair",
            "email": "invalid-email",  # Invalid email format
            "passphrase": "secretpassphrase"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)  



    def test_create_keypair_duplicate_name(self):
        self.client.force_authenticate(self.user)
        data = {
            "name": "test_keypair",
            "email": "testuser@example.com",
            "passphrase": "secretpassphrase"
        }

        self.client.post(self.url, data, format='json')
        
        # Try to create another with the same name
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  
        self.assertIn('name', response.data) 


    def test_create_keypair_missing_name(self):
        self.client.force_authenticate(self.user)
        data = {
            "email": "testuser@example.com",
            "passphrase": "secretpassphrase"
        }
        response = self.client.post(self.url, data, format='json')
        
        # Check that the keypair is created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(KeyPair.objects.count(), 1)
        keypair = KeyPair.objects.first()




    def test_create_keypair_missing_email(self):
        self.client.force_authenticate(self.user)
        data = {
            "name": "test_keypair",
            "passphrase": "secretpassphrase"
        }
        response = self.client.post(self.url, data, format='json')
        
        # Check that the keypair is created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(KeyPair.objects.count(), 1)
        keypair = KeyPair.objects.first()
        self.assertIsNotNone(keypair.name) # Assuming default name if not provided   


    def test_create_keypair_missing_name_and_email(self):
        self.client.force_authenticate(self.user)
        data = {
        }
        response = self.client.post(self.url, data, format='json')
        
        # Check that the keypair is created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(KeyPair.objects.count(), 1)
        keypair = KeyPair.objects.first()
        self.assertIsNotNone(keypair.name)
        



        
