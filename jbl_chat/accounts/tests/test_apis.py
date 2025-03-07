from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

class MyOtherUsersAPIViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create three users.
        self.user1 = User.objects.create_user(
            username='user1', password='password', first_name='Alice', email='alice@example.com'
        )
        self.user2 = User.objects.create_user(
            username='user2', password='password', first_name='Bob', email='bob@example.com'
        )
        self.user3 = User.objects.create_user(
            username='user3', password='password', first_name='Charlie', email='charlie@example.com'
        )
        # Authenticate as user1 (Alice).
        self.client.force_authenticate(user=self.user1)

    def test_list_excludes_authenticated_user_and_orders_by_first_name(self):

        url = reverse('my_other_users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        users_list = data.get('results', data)

        # Ensure the authenticated user is not in the returned list.
        for user in users_list:
            self.assertNotEqual(user['id'], self.user1.id)

        # Verify ordering by first_name ascending.
        # Expected order for the remaining users: Bob, Charlie.
        expected_first_names = sorted([self.user2.first_name, self.user3.first_name])
        actual_first_names = [user['first_name'] for user in users_list]
        self.assertEqual(actual_first_names, expected_first_names)