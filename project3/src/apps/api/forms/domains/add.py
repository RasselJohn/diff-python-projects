import logging
import math
from traceback import format_exc

import redis
from django import forms
from django.conf import settings
from django.contrib.postgres.forms import SimpleArrayField
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from src.apps.api.utils import get_base_domain

log = logging.getLogger('django.request')


class DomainsAddForm(forms.Form):
    links = SimpleArrayField(
        forms.CharField(max_length=100),
        min_length=1, label=_('Список урлов'),
        error_messages={'required': _('Список урлов не задан.'), 'invalid': _('Список урлов некорректен.')}
    )

    def save_urls(self):
        links = self.cleaned_data.get('links')

        try:
            timestamp = math.floor(timezone.now().timestamp())
            unique_domains = self.collect_unique_domains(links)

            redis_client = redis.Redis(**settings.REDIS_CONFIG)
            curr_id = redis_client.incr('curr_id')
            urls = {index: domain for index, domain in enumerate(unique_domains, start=curr_id)}

            # set curr_id for next saving in 'sites' hash table
            redis_client.incr('curr_id', len(urls))

            # save sites in hash table -> pk:domain
            redis_client.hmset('sites', urls)

            # save timestamps in sorted set -> timestamps:sites_pk
            redis_client.zadd('timestamps', {pk: timestamp for pk in urls.keys()}, nx=True)

        except Exception:
            log.error(f'Error: {format_exc()}')
            return None

        return timestamp

    @classmethod
    def collect_unique_domains(cls, urls):
        unique_urls = set()

        for url in urls:
            url = get_base_domain(url)
            if url:
                unique_urls.add(url)

        return unique_urls
