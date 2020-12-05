from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def get_form_errors(form) -> dict:
    errors_list = [''.join(e) for e in form.errors.values()]
    return {'error': ''.join(errors_list)}


def is_valid_password(password, password_repeat) -> bool:
    return password and password_repeat and password == password_repeat


def check_exist_email(email) -> None:
    if User.objects.filter(email__icontains=email).exists():
        raise ValidationError(_('Указанный Email уже зарегистрирован в системе.'), code='duplicate')


def check_exist_username(username) -> None:
    if User.objects.filter(username__icontains=username).exists():
        raise ValidationError(_('Указанный Email уже зарегистрирован в системе.'), code='duplicate')
