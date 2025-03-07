from django.urls import path
from .api_views import MyMessagesWithAPIView, MessageCreateAPIView

# The url prefix 'my'  is to indicate the api call is specific to that user calling it
urlpatterns = [
    path('my/messages_with/<int:user_id>/', MyMessagesWithAPIView.as_view(), name='my_messages_with'),
    path('my/message_create/', MessageCreateAPIView.as_view(), name='my_message_create'),
]