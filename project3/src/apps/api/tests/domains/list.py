import json
from typing import Any
from unittest.mock import patch

import redis
from django.conf import settings
from django.test import override_settings
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from rest_framework import status

from src.apps.api.serializers import DomainsListSerialilzer
from src.apps.api.tests.domains.base import TestDomainBaseView


class TestDomainListView(TestDomainBaseView):
    def get_url(self) -> str:
        return reverse_lazy('visited-domains')

    def test_empty_request(self):
        response: Any = self.client.get(self.get_url())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data: dict = json.loads(response.content)
        self.assertEqual(
            data,
            {'date_from': [_('Начальный период не задан.')], 'date_to': [_('Конечный период не задан.')]}
        )

    def test_absent_timestamp(self):
        with patch.object(DomainsListSerialilzer, 'get_domains', return_value=None):
            response: Any = self.client.get(
                self.get_url(),
                data={'date_from': 1, 'date_to': 10},
                content_type=self.content_type
            )
            self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)

            data = json.loads(response.content)
            self.assertIn('status', data)
            self.assertEqual(data['status'], _('Ошибка сервера. Пожалуйста, обратитесь позже.'))

    def test_incorrect_periods(self):
        response: Any = self.client.get(self.get_url(), data={'date_from': 100, 'date_to': 10})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            {'non_field_errors': [_('Конечный период не может быть меньше начального.')]},
            json.loads(response.content)
        )

    @override_settings(REDIS_CONFIG=settings.TEST_REDIS_CONFIG)
    def test_correct_request(self):
        # request on addition to db
        addition_response: Any = self.client.post(
            reverse_lazy('visited-links'),
            data=json.dumps(self.test_links),
            content_type=self.content_type
        )
        self.assertEqual(addition_response.status_code, status.HTTP_200_OK)

        result: dict = json.loads(addition_response.content)
        timestamp: int = result.get('timestamp')
        date_from: int = timestamp - 10
        date_to: int = timestamp + 10

        # request on getting from db
        getting_response: Any = self.client.get(
            self.get_url(),
            data={'date_from': date_from, 'date_to': date_to},
            content_type=self.content_type
        )
        self.assertEqual(getting_response.status_code, status.HTTP_200_OK)

        result: dict = json.loads(getting_response.content)
        self.assertIn('domains', result)

        domains = result.get('domains')
        redis_client = redis.Redis(host=settings.REDIS_HOST, **settings.TEST_REDIS_CONFIG)

        # check quantity
        sites_pk: set = redis_client.zrangebyscore('timestamps', date_from, date_to)
        self.assertEqual(len(sites_pk), len(domains))

        # check an identity of collections
        urls: list = redis_client.hmget('sites', sites_pk)
        self.assertCountEqual(urls, domains)

        redis_client.delete('curr_id', 'timestamps', 'sites')
