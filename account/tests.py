from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


# Todo test for User model
# assert for token lenght and is_verified


class RegisterTestCase(APITestCase):
    def test_create_account(self) -> None:

        data = {
            "username": "idan",
            "email": "idan@gmail.com",
            "password": "password22",
            "first_name": "hwhd",
            "last_name": "dfjjfje",
            "address": "4,Lagos Nigeria",
            "phone_number": "+2348102045787",
        }

        url = reverse("account:user-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertLessEqual(len(User.objects.get().token), 60)
        self.assertEqual(User.objects.get().username, "idan")
        self.assertFalse(response.data.get("is_verified"))


class LoginTestCase(APITestCase):
    def setUp(self) -> None:
        existing_data = {
            "email": "active@gmail.com",
            "username": "fagbo",
            "password": "password123",
            "is_verified": True,
        }
        user = User.objects.create_user(**existing_data)

    def test_login_user(self):
        login_data = {"email": "active@gmail.com", "password": "password123"}

        url = reverse("account:user-login_user")
        response = self.client.post(url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
