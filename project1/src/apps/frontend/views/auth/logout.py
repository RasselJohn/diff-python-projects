from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('index'))
