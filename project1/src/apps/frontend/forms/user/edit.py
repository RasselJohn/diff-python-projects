from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from src.apps.frontend.utils import is_valid_password, check_exist_username, check_exist_email


class UserEditForm(forms.Form):
    first_name = forms.CharField(max_length=30, label=_('Имя'))

    last_name = forms.CharField(max_length=150, label=_('Фамилия'))

    username = forms.CharField(
        label=_('Логин'), max_length=150, error_messages={'required': _('Логин не задан.')}
    )

    email = forms.EmailField(
        label=_('Email'), error_messages={'required': _('Email не задан.'), 'invalid': _('Email некорректен.')},
    )

    password = forms.CharField(max_length=20, label=_('Пароль'), required=False)

    password_repeat = forms.CharField(max_length=20, label=_('Повтор пароля'), required=False)

    is_staff = forms.BooleanField(label=_('Полные права ?'), required=False)

    def __init__(self, user, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_email(self):
        email: str = self.cleaned_data.get('email')

        # if email was changed
        if self.user.email != email:
            # if other user has this email
            check_exist_email(email)

        return email

    def clean_username(self) -> str:
        username: str = self.cleaned_data.get('username')

        # if username was changed
        if self.user.username != username:
            # if other user has this username
            check_exist_username(username)

        return username

    def clean(self):
        password: str = self.cleaned_data.get('password')
        password_repeat: str = self.cleaned_data.get('password_repeat')
        if password or password_repeat:
            is_valid_password(self.cleaned_data.get('password'), self.cleaned_data.get('password_repeat'))

        return self.cleaned_data

    def edit_user(self) -> None:
        user: User = self.user
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.is_staff = self.cleaned_data.get('is_staff', False)

        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)

        user.save()
