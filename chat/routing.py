from django.urls import re_path, path

from . import consumers
from .consumers import OneConsumer
websocket_urlpatterns = [
    re_path(r"ws/socket-server", consumers.chatConsumer.as_asgi()),
    path('ws/two_url/', consumers.TwoConsumer.as_asgi()),
    path("ws/any_url/", OneConsumer.as_asgi())

]