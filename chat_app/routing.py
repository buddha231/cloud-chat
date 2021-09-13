from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'wss/chat/(?P<id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    ]
