from typing import Optional

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_('Логин'), error_messages={'required': _('Логин не задан.'), 'invalid': _('Логин некорректен.')}
    )

    password = forms.CharField(max_length=20, label=_('Пароль'))

    def clean(self) -> dict:
        cleaned_data: dict = super(LoginForm, self).clean()

        username: str = cleaned_data.get('username')
        password: str = cleaned_data.get('password')
        if not username or not password:
            raise ValidationError(_('Логин и/или пароль не заданы.'), code='invalid')

        user: Optional[User] = authenticate(username=username, password=password)
        if not user:
            raise ValidationError(_('Введены неккоректные логин или пароль.'), code='invalid')

        cleaned_data['user'] = user
        return cleaned_data

    def get_user(self):
        return self.cleaned_data.get('user')
