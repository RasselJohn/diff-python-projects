from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from src.apps.frontend.utils import is_valid_password


class UserEditForm(forms.Form):
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

    password = forms.CharField(max_length=20, label=_('Пароль'), required=False)

    password_repeat = forms.CharField(max_length=20, label=_('Повтор пароля'), required=False)

    is_staff = forms.BooleanField(label=_('Полные права ?'), required=False)

    def __init__(self, user, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.user = user

    def edit_user(self):
        user = self.user
        email = self.cleaned_data.get('email').lower()
        if email != user.email:
            user.email = email

        username = self.cleaned_data.get('username')
        if username != user.username:
            user.username = username

        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.is_staff = self.cleaned_data.get('is_staff', False)

        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)

        user.save()

    def clean(self):
        password = self.cleaned_data.get('password')
        if not password:
            return self.cleaned_data

        password_repeat = self.cleaned_data.get('password_repeat')

        if not is_valid_password(password, password_repeat):
            raise ValidationError(_('Пароли некорректны или не совпадают.'), code='invalid')

        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise ValidationError(
                _('Указанный Email уже зарегистрирован в системе.'), code='duplicate'
            )

        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise ValidationError(
                _('Указанный логин уже зарегистрирован в системе.'), code='duplicate'
            )

        return username
