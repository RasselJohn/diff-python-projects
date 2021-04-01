import redis
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels_redis.core import RedisChannelLayer
from django.conf import settings
from django.core.management import BaseCommand

from src.apps.currency.consumers import CurrencyConsumer


class Command(BaseCommand):
    help = 'Check admin currency.'

    # Redis does not allow to set callback for expire data.
    def handle(self, *args, **options) -> None:
        print('Run checking currency...')
        redis_store = redis.StrictRedis(**settings.REDIS_SETTINGS)

        while True:
            if redis_store.get('admin_currency_rate_exists'):
                admin_currency_rate: bytes = redis_store.get('admin_currency_rate')

                # admin_currency_rate does not expire yet
                if admin_currency_rate:
                    continue

                redis_store.delete('admin_currency_rate_exists')

                # send signal to channel
                print('Send signal to channel...')
                channel_layer: RedisChannelLayer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    CurrencyConsumer.group_name, {"type": "set_currency_from_aside"}
                )
