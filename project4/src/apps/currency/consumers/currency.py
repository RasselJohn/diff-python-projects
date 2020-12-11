import json
from django.utils import timezone

import redis
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from dateutil import parser
from django.conf import settings


class CurrencyConsumer(AsyncJsonWebsocketConsumer):
    group_name = 'currency_group'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # init redis
        self.redis_store = redis.StrictRedis(**settings.REDIS_SETTINGS)

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.get_currency_rate()

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        print(f'We are received: {text_data}')
        await self.set_currency_rate_from_admin(json.loads(text_data))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.close(close_code)

    async def get_currency_rate(self):
        admin_currency_rate = self.redis_store.get('admin_currency_rate')
        if admin_currency_rate:
            await self.channel_layer.group_send(
                self.group_name,
                {'type': 'send_currency', 'message': admin_currency_rate.decode()}
            )
            return

        remote_currency_rate = self.redis_store.get('remote_currency_rate')
        if remote_currency_rate:
            await self.channel_layer.group_send(
                self.group_name,
                {'type': 'send_currency', 'message': remote_currency_rate.decode()}
            )

    async def set_currency_from_aside(self, event):
        await self.get_currency_rate()

    async def set_currency_rate_from_admin(self, admin_rate):
        new_rate = admin_rate.get('newRate')
        self.redis_store.set('admin_currency_rate', new_rate)
        self.redis_store.set('admin_currency_rate_exists', 1)

        admin_currency_rates = self.redis_store.get('admin_currency_rates')
        if admin_currency_rates:
            self.redis_store.set('admin_currency_rates', '\n'.join([admin_currency_rates.decode(), str(new_rate)]))
        else:
            self.redis_store.set('admin_currency_rates', f'{new_rate}\n')

        await self.channel_layer.group_send(
            self.group_name,
            {'type': 'send_admin_currencies',
             'message': self.redis_store.get('admin_currency_rates').decode()}
        )

        last_period = parser.parse(admin_rate.get('expire')) - timezone.now()
        self.redis_store.expire('admin_currency_rate', last_period)
        await self.get_currency_rate()

    async def send_currency(self, event):
        await self.send(json.dumps({'currencyRate': event['message']}))

    async def send_admin_currencies(self, event):
        await self.send(json.dumps({'adminCurrencies': event['message']}))
