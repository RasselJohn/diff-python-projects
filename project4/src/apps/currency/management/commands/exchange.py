import json
import logging
import time
from traceback import format_exc
from urllib.request import urlopen

import redis
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.core.management import BaseCommand

from src.apps.currency.consumers import CurrencyConsumer

log = logging.getLogger(__name__)


# manage exchange
class Command(BaseCommand):
    help = 'Get USD/RUB exchange rate.'

    def handle(self, *args, **options):
        print('Upload rate...')

        while True:
            try:
                # load rate
                connect = urlopen(settings.USD_EXCHANGE_URL)
                response = json.loads(connect.read())
                rate = response.get('rates').get('RUB')
                print(f'New rate: {rate}')

                # add rate in redis
                self.redis_store = redis.StrictRedis(**settings.REDIS_SETTINGS)
                self.redis_store.set('remote_currency_rate', rate)

                # send signal to channel
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    CurrencyConsumer.group_name, {"type": "set_currency_from_aside"}
                )
            except Exception:
                print('Error:', format_exc())

            print(f'Upload complete!\nNext run after {settings.EXCHANGE_SLEEP_TIME // 60} minutes...')
            time.sleep(settings.EXCHANGE_SLEEP_TIME)
