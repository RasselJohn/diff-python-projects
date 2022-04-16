from typing import Optional

from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_('Логин'), max_length=150,
        error_messages={'required': _('Логин не задан.')}
    )

    password = forms.CharField(
        max_length=20,
        label=_('Пароль'),
        error_messages={'required': _('Логин не задан.')}
    )

    def clean(self) -> dict:
        username: str = self.cleaned_data.get('username')
        password: str = self.cleaned_data.get('password')
        user: Optional[User] = authenticate(
            username=username, password=password)

        if not user:
            raise ValidationError(_('Введены неккоректные логин или пароль.'), code='invalid')

        self.cleaned_data['user'] = user
        return self.cleaned_data

    def login(self, request: HttpRequest) -> None:
        login(request, self.cleaned_data.get('user'))
