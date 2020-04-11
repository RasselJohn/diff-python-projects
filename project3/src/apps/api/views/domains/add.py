import json

from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

from src.apps.api.forms import DomainsAddForm
from src.apps.api.utils import get_form_errors


class DomainsAddView(View):
    def post(self, request):
        form = DomainsAddForm(json.loads(request.body))
        if not form.is_valid():
            return JsonResponse(get_form_errors(form), status=400)

        result = form.save_urls()
        if result is None:
            return JsonResponse({'status': _('Ошибка сервера. Пожалуйста, обратитесь позже.')}, status=502)

        return JsonResponse({
            'timestamp': result,  # need for testing
            'status': 'ok'
        })
