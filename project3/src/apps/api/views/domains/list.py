from typing import Optional

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.api.serializers import DomainsListSerialilzer


class DomainsListView(ListAPIView):
    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = DomainsListSerialilzer(request.GET.copy())
        serializer.is_valid(raise_exception=True)

        result: Optional[set] = serializer.get_domains()
        if result is None:
            return Response(
                {'status': _('Ошибка сервера. Пожалуйста, обратитесь позже.')},
                status=status.HTTP_502_BAD_GATEWAY
            )

        return Response({'domains': list(result)})
