from django.urls import path
from .consumers import TokenAuthConsumer

websocket_urlpatterns = [
    path('admin/notification/' , TokenAuthConsumer.as_asgi()),
]