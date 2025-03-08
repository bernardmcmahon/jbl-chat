from django.urls import path
from .views import other_users, login_as_user

urlpatterns = [
    path('other_users/',other_users, name='other_users'),
    path('login_as/<int:user_id>/', login_as_user, name='login_as_user'),
]