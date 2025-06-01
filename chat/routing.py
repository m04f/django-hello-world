from django.urls import path

from .consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/chat/sessions/<uuid:session>/", ChatConsumer.as_asgi()),
]
