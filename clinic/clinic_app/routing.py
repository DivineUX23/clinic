from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from clinic_app.consumers import OrderConsumer  # Import your consumer
"""
application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/orders/", OrderConsumer.as_asgi()),
        ])
    ),
})
"""
websocket_urlpatterns = [
    path('ws/orders/', OrderConsumer.as_asgi()),
]