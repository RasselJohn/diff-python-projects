from django.http import JsonResponse, HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views import View

from src.apps.frontend.forms import LoginForm
from src.apps.frontend.utils import get_form_errors


class LoginView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            return JsonResponse({'url': reverse_lazy('users')})

        form = LoginForm(request.POST.copy())
        if not form.is_valid():
            return JsonResponse(get_form_errors(form))

        form.login(request)
        return JsonResponse({'url': reverse_lazy('users')})
