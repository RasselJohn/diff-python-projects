import json

import redis

from django.conf import settings
from django.test import override_settings
from django.urls import reverse_lazy

from src.apps.api.tests.domains.base import TestDomainBaseView


class TestDomainListView(TestDomainBaseView):
    url = reverse_lazy('visited-domains')

    def test_empty_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertIn('status', json.loads(response.content))

    def test_incorrect_periods(self):
        response = self.client.get(self.url, data={'date_from': 100, 'date_to': 10}, )
        self.assertEqual(response.status_code, 400)
        self.assertIn('status', json.loads(response.content))

    @override_settings(REDIS_CONFIG=settings.TEST_REDIS_CONFIG)
    def test_correct_request(self):
        # request on addition to db
        addition_response = self.client.post(
            reverse_lazy('visited-links'), data=json.dumps(self.test_links), content_type=self.content_type
        )
        self.assertEqual(addition_response.status_code, 200)

        result = json.loads(addition_response.content)
        timestamp = result.get('timestamp')
        date_from = timestamp - 10
        date_to = timestamp + 10

        # request on getting from db
        getting_response = self.client.get(
            self.url, data={'date_from': date_from, 'date_to': date_to}, content_type=self.content_type
        )
        self.assertEqual(getting_response.status_code, 200)

        result = json.loads(getting_response.content)
        self.assertIn('domains', result)
        domains = result.get('domains')

        redis_client = redis.Redis(**settings.TEST_REDIS_CONFIG)

        # check quantity
        sites_pk = redis_client.zrangebyscore('timestamps', date_from, date_to)
        self.assertEqual(len(sites_pk), len(domains))

        # check an identity of collections
        urls = redis_client.hmget('sites', sites_pk)
        self.assertCountEqual(urls, domains)

        redis_client.delete('curr_id', 'timestamps', 'sites')
