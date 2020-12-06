from typing import Union

from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View


class IndexView(View):
    template_name = 'index.html'

    def get(self, request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('users'))

        return render(request, self.template_name)
