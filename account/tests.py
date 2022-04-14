
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterTestCase(APITestCase):
    def test_register(self):
        """
        Ensure we can register a new account object.
        """
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'newuser@email.com',
            'password': 'NewUser===123',
            'password': 'NewUser===123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="newuser",
                                             password="NewUser===123")

    def test_login(self):
        data = {
            "username": "newuser",
            "password": "NewUser===123"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # using token authentication test for now, jwt test is complex so will do it later
    def test_logout(self):
        self.token = Token.objects.get(user__username='newuser')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    # ...
