from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from src.apps.frontend.utils import is_valid_password


class UserAddForm(forms.Form):
    first_name = forms.CharField(max_length=100, label=_('Имя'),
                                 error_messages={'required': _('Имя не задано.')})

    last_name = forms.CharField(max_length=200, label=_('Фамилия'),
                                error_messages={'required': _('Фамилия не задана.')})

    username = forms.CharField(
        label=_('Логин'),
        error_messages={'required': _('Логин не задан.'), 'invalid': _('Логин некорректен.')}
    )

    email = forms.EmailField(
        label=_('Email'),
        error_messages={'required': _('Email не задан.'), 'invalid': _('Email некорректен.')}
    )

    password = forms.CharField(
        max_length=20, label=_('Пароль'), error_messages={'required': _('Пароль не задан.')})

    password_repeat = forms.CharField(max_length=20, label=_('Повтор пароля'),
                                      error_messages={'required': _('Повтор пароля не задан.')})

    is_staff = forms.BooleanField(label=_('Полные права ?'), required=False)

    def add_user(self):
        email = self.cleaned_data.get('email').lower()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        is_staff = self.cleaned_data.get('is_staff', False)

        user = User.objects.create_user(
            username, email, password, first_name=first_name, last_name=last_name
        )

        if is_staff:
            user.is_staff = is_staff
            user.save()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                _('Указанный Email уже зарегистрирован в системе.'), code='duplicate'
            )

        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                _('Указанный логин уже зарегистрирован в системе.'), code='duplicate'
            )

        return username

    def clean(self):
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')

        if not is_valid_password(password, password_repeat):
            raise ValidationError(_('Пароли некорректны или не совпадают.'), code='invalid')

        return self.cleaned_data
