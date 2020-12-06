from django.contrib.auth.models import User
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from src.apps.frontend.forms import UserEditForm
from src.apps.frontend.utils import get_form_errors


class UserEditView(View):
    template_name = 'user-edit.html'

    def get(self, request: HttpRequest, user_id: str) -> HttpResponse:
        user: User = get_object_or_404(User, pk=user_id)
        return render(request, self.template_name, {'user_detail': user})

    def post(self, request: HttpRequest, user_id: str) -> JsonResponse:
        user: User = get_object_or_404(User, pk=user_id)
        form = UserEditForm(user, request.POST.copy())

        if not form.is_valid():
            return JsonResponse(get_form_errors(form))

        form.edit_user()
        return JsonResponse({'url': reverse_lazy('users')})
