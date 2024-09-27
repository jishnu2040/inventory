from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.login_url = reverse('login')  # Adjust to your login URL

    def test_user_login(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser', 
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # Checking if JWT token is returned
