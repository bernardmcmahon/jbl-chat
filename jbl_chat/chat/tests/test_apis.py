from django.test import TestCase, override_settings
from django.urls import path, reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta


from ..api_views import MyMessagesWithAPIView, MessageCreateAPIView
from ..models import Message

User = get_user_model()

# # Temporary URL configuration for tests.
# urlpatterns = [
#     # URL for the messages with view, expects the other user's id.
#     path('api/messages_with/<int:user_id>/', MyMessagesWithAPIView.as_view(), name='messages-with'),
#     # URL for the message create view.
#     path('api/messages/create/', MessageCreateAPIView.as_view(), name='my_message_create'),
# ]
#
#
# @override_settings(ROOT_URLCONF=__name__)
class MessagesAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create two users.
        self.user1 = User.objects.create_user(
            username='user1', password='password', first_name='Alice', email='alice@example.com'
        )
        self.user2 = User.objects.create_user(
            username='user2', password='password', first_name='Bob', email='bob@example.com'
        )
        # Authenticate as user1.
        self.client.force_authenticate(user=self.user1)

        # Create three messages between user1 and user2 with different sent_at times.
        self.message1 = Message.objects.create(
            sender=self.user1,
            recipient=self.user2,
            content='Hello from user1 to user2',
            sent_at=timezone.now() - timedelta(minutes=5)
        )
        self.message2 = Message.objects.create(
            sender=self.user2,
            recipient=self.user1,
            content='Reply from user2 to user1',
            sent_at=timezone.now() - timedelta(minutes=3)
        )
        self.message3 = Message.objects.create(
            sender=self.user1,
            recipient=self.user2,
            content='Another message from user1',
            sent_at=timezone.now() - timedelta(minutes=1)
        )

    def test_my_messages_with_api(self):
        """
        Test that MyMessagesWithAPIView returns messages between the authenticated user and the specified other user,
        ordered by newest first (i.e. descending by sent_at).
        """
        url = reverse('my_messages_with', kwargs={'user_id': self.user2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Since pagination is enabled, the messages might be under a 'results' key.
        messages = data.get('results', data)

        # Expected order: newest first.
        # Given our sent_at values, the expected order is message3, message2, message1.
        expected_order = [self.message3.id, self.message2.id, self.message1.id]
        actual_order = [msg['id'] for msg in messages]
        self.assertEqual(actual_order, expected_order)

    def test_messages_with_excludes_other_users_messages(self):
        """
        Test that MyMessagesWithAPIView only returns messages between user1 and user2.
        Messages involving other users (e.g. user3) should be excluded.
        """
        # Create a third user and a message between user1 and user3.
        user3 = User.objects.create_user(
            username='user3', password='password', first_name='Dave', email='dave@example.com'
        )
        Message.objects.create(
            sender=self.user1,
            recipient=user3,
            content='Message between user1 and user3',
            sent_at=timezone.now() - timedelta(minutes=2)
        )
        # Request messages_with for user2.
        url = reverse('my_messages_with', kwargs={'user_id': self.user2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        messages = data.get('results', data)

        # Check that each returned message is strictly between user1 and user2.
        for msg in messages:
            sender = msg.get('sender')['id']
            recipient = msg.get('recipient')['id']
            self.assertTrue(
                (sender == self.user1.id and recipient == self.user2.id) or
                (sender == self.user2.id and recipient == self.user1.id),
                msg=f"Unexpected message found: sender={sender}, recipient={recipient}  - message failed={msg}"
            )

    def test_message_create_api(self):
        """
        Test that MessageCreateAPIView accepts a valid POST payload and creates a message.
        """
        url = reverse('my_message_create')
        # Assuming MessageCreateSerializer expects fields 'recipient' and 'content'.
        payload = {
            'recipient_id': self.user2.id,
            'content': 'Test message from user1'
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, 201)
        # Verify the message was created with the correct sender, recipient, and content.
        message = Message.objects.filter(
            sender=self.user1,
            recipient=self.user2,
            content='Test message from user1'
        ).first()
        self.assertIsNotNone(message)