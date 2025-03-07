from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.pagination import LimitOffsetPagination

from .serializers import UserSerializer
User = get_user_model()

class MyOtherUsersAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        # Exclude the current user from the list
        return User.objects.exclude(id=self.request.user.id).order_by('first_name')