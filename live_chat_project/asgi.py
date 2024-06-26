import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import live_chat_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'live_chat_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            live_chat_app.routing.websocket_urlpatterns
        )
    ),
})
