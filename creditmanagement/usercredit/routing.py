from django.urls import path
from .consumers import  AdminNotificationConsumers

websocket_urlpatterns = [
    # path('admin/notification/' , TokenAuthConsumer.as_asgi()), # Only for testing purpose
    path('admin/notification/' , AdminNotificationConsumers.as_asgi()),
]