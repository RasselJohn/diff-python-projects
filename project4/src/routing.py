from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from src.apps.currency.consumers import CurrencyConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([path("ws/", CurrencyConsumer, name="currency")]),
})
