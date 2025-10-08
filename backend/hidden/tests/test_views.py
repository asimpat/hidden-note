from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from hidden.models import Message

User = get_user_model()


class HiddenNoteAPITest(APITestCase):
    def setUp(self):
        # Create a regular user
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.secret_link = self.user.secret_link
        self.client = APIClient()

        # URLs (updated to match your urls.py names)
        self.register_url = reverse('register')
        self.send_message_url = reverse(
            'send_message', kwargs={'secret_link': self.secret_link})
        self.message_list_url = reverse('messages')  # updated
        self.user_list_url = reverse('users')        # updated

    def test_register_user(self):
        """Test user registration endpoint"""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpass123"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)
        self.assertEqual(User.objects.count(), 2)

    def test_send_message(self):
        """Test sending a message via secret link"""
        data = {"message": "This is a hidden message"}
        response = self.client.post(self.send_message_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.first().user, self.user)

    def test_get_messages_authenticated_user(self):
        """Test that a logged-in user can see only their messages"""
        Message.objects.create(user=self.user, message="My message")

        # Authenticate
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.message_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['message'], "My message")

    def test_get_messages_unauthenticated_user(self):
        """Ensure unauthenticated users cannot access messages"""
        response = self.client.get(self.message_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_message(self):
        """Test deleting a message as owner"""
        msg = Message.objects.create(user=self.user, message="Delete me")

        self.client.force_authenticate(user=self.user)
        url = reverse('get_delete_message', kwargs={'id': msg.id})  # updated
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Message.objects.count(), 0)

    def test_user_list_public(self):
        """Anyone can view user list"""
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the paginated 'results' key
        self.assertIsInstance(response.data['results'], list)
