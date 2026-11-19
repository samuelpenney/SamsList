from django.urls import re_path  # ← must be from django.urls, NOT from django!
from . import consumers
# Exactly like urls.py but for WebSocket connections only
websocket_urlpatterns = [
    re_path(
        r'ws/chat/(?P<room_name>[-a-zA-Z0-9_]+)/$',
        consumers.ChatConsumer.as_asgi()
    ),
]