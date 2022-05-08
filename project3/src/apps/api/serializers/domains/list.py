import logging
from traceback import format_exc
from typing import Optional

import redis
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

log = logging.getLogger('django.request')


class DomainsListSerialilzer(serializers.Serializer):
    date_from = serializers.IntegerField(
        min_value=0,
        label=_('Начальный период (в секундах)'),
        error_messages={'required': _('Начальный период не задан.'), 'invalid': _('Начальный период некорректен.')}
    )

    date_to = serializers.IntegerField(
        min_value=0,
        label=_('Конечный период (в секундах)'),
        error_messages={'required': _('Конечный период не задан.'), 'invalid': _('Конечный период некорректен.')}
    )

    def validate(self, attrs) -> dict:
        # if 'date_from' and 'date_to' do not exist - base 'clean' method checked it and raises the errors later.
        date_from: int = attrs.get('date_from')
        date_to: int = attrs.get('date_to')
        if date_to and date_from and date_to < date_from:
            raise serializers.ValidationError(_('Конечный период не может быть меньше начального.'))

        return attrs

    def get_domains(self) -> Optional[set]:
        date_from: int = self.validated_data.get('date_from')
        date_to: int = self.validated_data.get('date_to')
        sites_pk: Optional[set] = None

        try:
            redis_client = redis.Redis(host=settings.REDIS_HOST, **settings.REDIS_CONFIG)
            sites_pk = redis_client.zrangebyscore('timestamps', date_from, date_to)
            urls = redis_client.hmget('sites', sites_pk) if sites_pk else []
        except Exception:
            print(f"Error:", sites_pk, f"{format_exc()}")
            return

        return set(urls)
