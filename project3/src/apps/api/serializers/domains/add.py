import logging
import math
from traceback import format_exc
from typing import List, Optional

import redis
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from src.apps.api.utils import get_base_domain

log = logging.getLogger('django.request')


class DomainsAddSerializer(serializers.Serializer):
    links = serializers.ListField(
        child=serializers.CharField(max_length=100),
        min_length=1,
        label=_('Список Url'),
        error_messages={'required': _('Список Url не задан.'), 'invalid': _('Список Url некорректен.')}
    )

    def save_urls(self) -> Optional[int]:
        links: List[str] = self.validated_data.get('links')

        try:
            timestamp: int = math.floor(timezone.now().timestamp())
            unique_domains = self.collect_unique_domains(links)

            redis_client = redis.Redis(host=settings.REDIS_HOST, **settings.REDIS_CONFIG)
            curr_id: int = redis_client.incr('curr_id')
            urls = {index: domain for index, domain in enumerate(unique_domains, start=curr_id)}

            # set curr_id for next saving in 'sites' hash table
            redis_client.incr('curr_id', len(urls))

            # save sites in hash table -> pk:domain
            redis_client.hset('sites', mapping=urls)

            # save timestamps in sorted set -> timestamps:sites_pk
            redis_client.zadd('timestamps', {pk: timestamp for pk in urls.keys()}, nx=True)

        except Exception:
            print(f'Error: {format_exc()}')
            return

        return timestamp

    @classmethod
    def collect_unique_domains(cls, urls: list) -> set:
        return {url for u in urls if (url := get_base_domain(u))}
