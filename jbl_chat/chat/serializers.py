from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message
from accounts.serializers import UserSerializer
User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'content', 'sent_at', 'sender', 'recipient']


class MessageCreateSerializer(serializers.ModelSerializer):
    # Accept recipient id as input when creating a message
    recipient_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Message
        fields = ['id', 'content', 'recipient_id']

    def create(self, validated_data):
        request = self.context.get('request')
        recipient_id = validated_data.pop('recipient_id')
        # Validate recipient existence
        try:
            recipient = User.objects.get(id=recipient_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Recipient does not exist")
        message = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            **validated_data
        )
        return message