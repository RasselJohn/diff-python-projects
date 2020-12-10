import logging
from traceback import format_exc
from typing import Optional

import redis
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

log = logging.getLogger('django.request')


class DomainsListForm(forms.Form):
    date_from = forms.IntegerField(
        required=True,
        label=_('Начальный период (в секундах)'), min_value=0,
        error_messages={'required': _('Начальный период не задан.'), 'invalid': _('Начальный период некорректен.')}
    )

    date_to = forms.IntegerField(
        required=True,
        label=_('Конечный период (в секундах)'), min_value=0,
        error_messages={'required': _('Конечный период не задан.'), 'invalid': _('Конечный период некорректен.')}
    )

    def clean(self) -> dict:
        cleaned_data: dict = super(DomainsListForm, self).clean()

        # if 'date_from' and 'date_to' do not exist - base 'clean' method checked it and raises the errors later.
        date_from: int = cleaned_data.get('date_from')
        date_to: int = cleaned_data.get('date_to')
        if date_to and date_from and cleaned_data.get('date_to') < cleaned_data.get('date_from'):
            raise forms.ValidationError(_('Конечный период не может быть меньше начального.'))

        return cleaned_data

    def get_domains(self) -> Optional[set]:
        date_from: int = self.cleaned_data.get('date_from')
        date_to: int = self.cleaned_data.get('date_to')

        try:
            redis_client = redis.Redis(host=settings.REDIS_HOST, **settings.REDIS_CONFIG)
            sites_pk: set = redis_client.zrangebyscore('timestamps', date_from, date_to)
            urls: list = redis_client.hmget('sites', sites_pk)
        except Exception:
            log.error(f'Error: {format_exc()}')
            return None

        return set(urls)
