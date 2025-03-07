from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# A simple API view for testing

class TestMessagesView(APIView):
    permission_classes = [AllowAny]  # Ensure no authentication blocks GET

    def get(self, request, *args, **kwargs):
        return Response({"detail": "Success"})

# A temporary URL configuration for the test
urlpatterns = [
    path('api/messages/', TestMessagesView.as_view(), name='messages'),
]


@override_settings(
    # Use the URLs defined in this module
    ROOT_URLCONF=__name__,
)
class AcceptHeaderVersioningTests(TestCase):
    """Test the current versioning system of the API"""
    def setUp(self):
        self.client = APIClient()

    def test_default_accept_header_version(self):
        # Send a request with the correct version in the Accept header
        response = self.client.get('/api/messages/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"detail": "Success"})

    def test_correct_accept_header_version(self):
        # Send a request with the correct version in the Accept header
        response = self.client.get('/api/messages/', HTTP_ACCEPT='application/json; version=1.0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"detail": "Success"})

    def test_incorrect_accept_header_version(self):
        # Send a request with an incorrect version (e.g., version 2.0)
        response = self.client.get('/api/messages/', HTTP_ACCEPT='application/json; version=2.0')
        self.assertEqual(response.status_code, 406)