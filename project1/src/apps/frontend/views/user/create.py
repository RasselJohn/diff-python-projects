from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from src.apps.frontend.forms import UserCreateForm
from src.apps.frontend.utils import get_form_errors


class UserCreateView(View):
    template_name = 'user-create.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name)

    def post(self, request: HttpRequest) -> JsonResponse:
        form = UserCreateForm(request.POST.copy())

        if not form.is_valid():
            return JsonResponse(get_form_errors(form))

        form.create()
        return JsonResponse({'url': reverse_lazy('users')})
