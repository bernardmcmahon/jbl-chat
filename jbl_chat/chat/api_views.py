from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.pagination import LimitOffsetPagination

from .models import Message
from .serializers import UserSerializer, MessageSerializer, MessageCreateSerializer

User = get_user_model()


class MyMessagesWithAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        # Expecting the other user's id as part of the URL
        other_user_id = self.kwargs.get('user_id')
        user = self.request.user
        # Retrieve messages where the user is either the sender or the recipient - currently ordered by newest
        return Message.objects.filter(
            Q(sender=user, recipient_id=other_user_id) | Q(sender_id=other_user_id, recipient=user)
        ).order_by('-sent_at')

class MessageCreateAPIView(generics.CreateAPIView):
    serializer_class = MessageCreateSerializer
    permission_classes = [permissions.IsAuthenticated]