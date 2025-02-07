from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status


class CustomTestClient(APIClient):
    def get(self, path, **extra):
        if "HTTP_HOST" not in extra:
            extra["HTTP_HOST"] = "pm:8000"
        return super().get(path, **extra)

    def post(self, path, data=None, **extra):
        if "HTTP_HOST" not in extra:
            extra["HTTP_HOST"] = "pm:8000"
        return super().post(path, data, **extra)

    def put(self, path, data=None, **extra):
        if "HTTP_HOST" not in extra:
            extra["HTTP_HOST"] = "pm:8000"
        return super().put(path, data, **extra)

    def delete(self, path, **extra):
        if "HTTP_HOST" not in extra:
            extra["HTTP_HOST"] = "pm:8000"
        return super().delete(path, **extra)



class RandomPasswordCreateViewTest(APITestCase):
    
    def setUp(self):
        self.client=CustomTestClient()
        self.url = "/api/passwords/generate-random/"

    def test_generate_random_password_success(self):
        data = {
            "length": 12,
            "is_alphabets": True,
            "is_lowercase": True,
            "is_uppercase": True,
            "is_numeric": True,
            "is_special": True,
        }
        
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("password", response.data)
        self.assertEqual(len(response.data["password"]), 12)

    def test_generate_random_password_no_character_types(self):
        data = {
            "length": 12,
            "is_alphabets": False,
            "is_lowercase": False,
            "is_uppercase": False,
            "is_numeric": False,
            "is_special": False,
        }
        
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("At least one character type must be selected.", str(response.data))

    def test_generate_random_password_length_too_short(self):
        data = {
            "length": 5,
            "is_alphabets": True,
            "is_lowercase": True,
            "is_uppercase": True,
            "is_numeric": True,
            "is_special": True,
        }
        
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("length must be 10 or greater", str(response.data))
