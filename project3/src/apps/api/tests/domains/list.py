import json
from typing import Any

import redis

from django.conf import settings
from django.test import override_settings
from django.urls import reverse_lazy
from rest_framework import status

from src.apps.api.tests.domains.base import TestDomainBaseView


class TestDomainListView(TestDomainBaseView):
    url: str = reverse_lazy('visited-domains')

    def test_empty_request(self) -> None:
        response: Any = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status', json.loads(response.content))

    def test_incorrect_periods(self) -> None:
        response: Any = self.client.get(self.url, data={'date_from': 100, 'date_to': 10}, )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status', json.loads(response.content))

    @override_settings(REDIS_CONFIG=settings.TEST_REDIS_CONFIG)
    def test_correct_request(self) -> None:
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
            self.url,
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
