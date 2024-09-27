from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient  # Import APIClient for DRF tests
from api.models import Item
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class ItemAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()  # Use APIClient instead of Django's TestCase client
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        
        # Get the JWT tokens for the user
        refresh = RefreshToken.for_user(self.user)
        
        # Set the Authorization header for the client
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Example item data for creating or updating items in the tests
        self.item_data = {'name': 'Test Item', 'description': 'This is a test item.'}

    def test_item_create(self):
        response = self.client.post(reverse('item-list-create'), self.item_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

