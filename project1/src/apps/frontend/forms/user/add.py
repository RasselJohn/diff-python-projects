from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from src.apps.frontend.utils import is_valid_password, check_exist_email, check_exist_username


class UserAddForm(forms.Form):
    first_name = forms.CharField(
        max_length=30, label=_('Имя'), error_messages={'required': _('Имя не задано.')}
    )

    last_name = forms.CharField(
        max_length=150, label=_('Фамилия'), error_messages={'required': _('Фамилия не задана.')}
    )

    username = forms.CharField(
        label=_('Логин'), max_length=150,
        validators=[check_exist_username],
        error_messages={'required': _('Логин не задан.')},
    )

    email = forms.EmailField(
        label=_('Email'), validators=[check_exist_email],
        error_messages={
            'required': _('Email не задан.'),
            'invalid': _('Email некорректен.')
        },
    )

    password = forms.CharField(
        max_length=20, label=_('Пароль'), error_messages={'required': _('Пароль не задан.')}
    )

    password_repeat = forms.CharField(
        max_length=20, label=_('Повтор пароля'), error_messages={'required': _('Повтор пароля не задан.')}
    )

    is_staff = forms.BooleanField(label=_('Полные права ?'), required=False)

    def clean(self) -> dict:
        is_valid_password(
            self.cleaned_data.get('password'),
            self.cleaned_data.get('password_repeat')
        )

        return self.cleaned_data

    def add_user(self) -> None:
        User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),

            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            is_staff=self.cleaned_data.get('is_staff', False)
        )
