import json
from typing import Optional

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.api.serializers import DomainsAddSerializer


class DomainsAddView(APIView):
    def post(self, request: Request) -> Response:
        serializer = DomainsAddSerializer(json.loads(request.body))
        serializer.is_valid(raise_exception=True)

        timestamp: Optional[float] = serializer.save_urls()
        if timestamp is None:
            return Response(
                {'status': _('Ошибка сервера. Пожалуйста, обратитесь позже.')},
                status=status.HTTP_502_BAD_GATEWAY
            )

        return Response({'timestamp': timestamp})
