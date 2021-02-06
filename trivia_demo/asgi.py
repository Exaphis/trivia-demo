"""
ASGI config for trivia_demo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import trivia_socket.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trivia_demo.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            trivia_socket.routing.websocket_urlpatterns
        )
    ),
})
