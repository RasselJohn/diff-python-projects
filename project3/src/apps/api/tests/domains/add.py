import json
from typing import Any
from unittest.mock import MagicMock, patch

import redis
from django.conf import settings
from django.test import override_settings
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from rest_framework import status

from src.apps.api.serializers import DomainsAddSerializer
from src.apps.api.tests.domains.base import TestDomainBaseView


class TestDomainAddView(TestDomainBaseView):
    def get_url(self) -> str:
        return reverse_lazy('visited-links')

    def test_empty_request(self):
        response: Any = self.client.post(self.get_url(), content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = json.loads(response.content)
        self.assertIn('links', data)
        self.assertEqual(data['links'][0], _('Список Url не задан.'))

    def test_absent_timestamp(self):
        with patch.object(DomainsAddSerializer, 'save_urls', return_value=None):
            response: Any = self.client.post(
                self.get_url(),
                data=json.dumps(self.test_links),
                content_type=self.content_type
            )
            self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)

            data = json.loads(response.content)
            self.assertIn('status', data)
            self.assertEqual(data['status'], _('Ошибка сервера. Пожалуйста, обратитесь позже.'))

    @override_settings(REDIS_CONFIG=settings.TEST_REDIS_CONFIG)
    def test_correct_request(self):
        response: Any = self.client.post(
            self.get_url(),
            data=json.dumps(self.test_links),
            content_type=self.content_type
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result: dict = json.loads(response.content)
        self.assertIn('timestamp', result)

        timestamp: int = result.get('timestamp')
        redis_client = redis.Redis(host=settings.REDIS_HOST, **settings.TEST_REDIS_CONFIG)

        sites_pk: set = redis_client.zrangebyscore('timestamps', timestamp, timestamp)
        self.assertEqual(len(sites_pk), 3)

        urls: list = redis_client.hmget('sites', sites_pk)
        self.assertEqual(len(urls), 3)

        sites_pk = redis_client.zrangebyscore('timestamps', timestamp - 5, timestamp - 1)
        self.assertEqual(len(sites_pk), 0)

        redis_client.delete('curr_id', 'timestamps', 'sites')
