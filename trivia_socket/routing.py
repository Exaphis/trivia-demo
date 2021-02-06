from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/quiz', consumers.GameConsumer.as_asgi()),
]