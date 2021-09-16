from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r'chat/<str:nickname>/', consumers.ChatConsumer.as_asgi()),
    path(r'time/', consumers.Time.as_asgi())
]