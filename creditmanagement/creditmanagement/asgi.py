"""
ASGI config for creditmanagement project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
# from channels.auth import AuthMiddlewareStack
from core.middleware import TokenAuthMiddleware


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'creditmanagement.settings')
# from core.routing import websocket_urlpatterns
import core.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(
        URLRouter(
            core.routing.websocket_urlpatterns
        ) 
    ) 
})

