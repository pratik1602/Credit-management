# chat/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # path('ws/sync/', consumers.MySyncConsumer.as_asgi()),
    # path('ws/async/', consumers.MyAsyncConsumer.as_asgi()),


    # path('ws/notification/', consumers.MyNotificationConsumer.as_asgi()),

    #----------------- GENERIC CONSUMERS ------------------#

    #------- WEBSOCKET AND ASYNC WEBSOCKET CONSUMER ------------#

    path('ws/wsync/', consumers.MySyncWebsocketConsumer.as_asgi()),    
    path('ws/wasync/', consumers.MyAsyncWebsocketConsumer.as_asgi()),

]