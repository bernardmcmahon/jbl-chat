from django.urls import path
from .api_views import MyOtherUsersAPIView

# The url prefix 'my'  is to indicate the api call is specific to that user calling it

urlpatterns = [
    path('my/other_users/', MyOtherUsersAPIView.as_view(), name='my_other_users'),

]