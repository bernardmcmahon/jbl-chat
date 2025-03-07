from django.db import models
from django.conf import settings

class Message(models.Model):
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_messages',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'From {self.sender} to {self.recipient} at {self.sent_at}'