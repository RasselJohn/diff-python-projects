from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View

from src.apps.frontend.forms import UserAddForm
from src.apps.frontend.utils import get_form_errors


class UserAddView(View):
    template_name = 'user-add.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = UserAddForm(request.POST.copy())

        if not form.is_valid():
            return JsonResponse(get_form_errors(form))

        form.add_user()
        return JsonResponse({'url': reverse_lazy('users')})
