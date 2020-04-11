import json

import redis
from django.conf import settings
from django.test import override_settings
from django.urls import reverse_lazy

from src.apps.api.tests.domains.base import TestDomainBaseView


class TestDomainAddView(TestDomainBaseView):
    url = reverse_lazy('visited-links')

    def test_empty_request(self):
        response = self.client.post(self.url, content_type=self.content_type)
        self.assertEqual(response.status_code, 400)
        self.assertIn('status', json.loads(response.content))

    @override_settings(REDIS_CONFIG=settings.TEST_REDIS_CONFIG)
    def test_correct_request(self):
        response = self.client.post(self.url, data=json.dumps(self.test_links), content_type=self.content_type)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        self.assertIn('status', result)
        self.assertIn('timestamp', result)
        self.assertIn('ok', result.get('status'))

        timestamp = result.get('timestamp')

        redis_client = redis.Redis(**settings.TEST_REDIS_CONFIG)

        sites_pk = redis_client.zrangebyscore('timestamps', timestamp, timestamp)
        self.assertEqual(len(sites_pk), 3)

        urls = redis_client.hmget('sites', sites_pk)
        self.assertEqual(len(urls), 3)

        sites_pk = redis_client.zrangebyscore('timestamps', timestamp - 5, timestamp - 1)
        self.assertEqual(len(sites_pk), 0)

        redis_client.delete('curr_id', 'timestamps', 'sites')
