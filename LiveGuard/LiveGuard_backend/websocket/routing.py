from django.urls import path
from .consumers import FrameConsumer

websocket_urlpatterns = [
    path('ws/', FrameConsumer.as_asgi()),  # WebSocket 경로 설정
]

