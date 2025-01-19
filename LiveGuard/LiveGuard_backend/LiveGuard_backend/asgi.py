"""
ASGI config for LiveGuard_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
import websocket.routing
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from websocket.consumers import FrameConsumer  # Consumer 클래스 임포트
from django.urls import path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LiveGuard_backend.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP 요청 처리
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/", FrameConsumer.as_asgi()),  # WebSocket 경로 설정
        ])
    ),
})
