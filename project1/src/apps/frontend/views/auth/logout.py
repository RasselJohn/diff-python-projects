from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse_lazy
from django.views import View


class LogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponseRedirect:
        logout(request)
        return HttpResponseRedirect(reverse_lazy('index'))
