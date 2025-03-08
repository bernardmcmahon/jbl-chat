from django.urls import path
from .views import home_view, messages_with, add_message, new_messages_with

urlpatterns = [
    path('', home_view, name='home'),
    path('messages_with/<int:other_user_id>/', messages_with, name='messages_with'),
    path('new_messages_with/<int:other_user_id>/', new_messages_with, name='new_messages_with'),
    path("messages/add/", add_message, name="add_message"),

]