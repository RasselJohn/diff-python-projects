from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from src.apps.collection.consumers import CollectDataConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([path("ws/", CollectDataConsumer, name="collect_data")]),
})
