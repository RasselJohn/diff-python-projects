from typing import Optional

from django.http import JsonResponse, HttpRequest
from django.utils.translation import gettext_lazy as _
from django.views import View

from src.apps.api.forms import DomainsListForm
from src.apps.api.utils import get_form_errors


class DomainsListView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        form = DomainsListForm(request.GET.copy())
        if not form.is_valid():
            return JsonResponse(get_form_errors(form), status=400)

        result: Optional[set] = form.get_domains()
        if result is None:
            return JsonResponse({'status': _('Ошибка сервера. Пожалуйста, обратитесь позже.')}, status=502)

        return JsonResponse({'domains': list(result), 'status': 'ok'})
