from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View


class UserRemoveView(View):
    template_name = 'user-remove.html'

    def get(self, request, user_id):
        context = {'user_id': user_id}
        return render(request, self.template_name, context)

    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)

        # don't remove! just switch off
        user.is_active = False
        user.save()

        return JsonResponse({'url': reverse_lazy('users')})
