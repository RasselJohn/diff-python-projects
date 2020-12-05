from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from src.apps.frontend.utils import is_valid_password, check_exist_email, check_exist_username


class UserEditForm(forms.Form):
    first_name = forms.CharField(max_length=100, label=_('Имя'), required=False, )

    last_name = forms.CharField(max_length=200, label=_('Фамилия'), required=False, )

    username = forms.CharField(
        label=_('Логин'), error_messages={'invalid': _('Логин некорректен.')},
        required=False, validators=[check_exist_username]
    )

    email = forms.EmailField(
        label=_('Email'), error_messages={'invalid': _('Email некорректен.')},
        required=False, validators=[check_exist_email]
    )

    password = forms.CharField(max_length=20, label=_('Пароль'), required=False)

    password_repeat = forms.CharField(max_length=20, label=_('Повтор пароля'), required=False)

    is_staff = forms.BooleanField(label=_('Полные права ?'), required=False)

    def __init__(self, user, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        password: str = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')

        if not is_valid_password(password, password_repeat):
            raise ValidationError(_('Пароли некорректны или не совпадают.'), code='invalid')

        return self.cleaned_data

    def edit_user(self) -> None:
        user: User = self.user
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.is_staff = self.cleaned_data.get('is_staff', False)

        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)

        user.save()
