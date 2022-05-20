from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import Form
from django.utils.translation import gettext_lazy as _


def get_form_errors(form: Form) -> dict:
    errors_list = [''.join(e) for e in form.errors.values()]
    return {'error': ''.join(errors_list)}


def is_valid_password(password: str, password_repeat: str):
    if not password or not password_repeat or password != password_repeat:
        raise ValidationError(_('Пароли некорректны или несовпадают.'), code='invalid')


def check_exist_email(email: str):
    if User.objects.filter(email__icontains=email).exists():
        raise ValidationError(_('Указанный email уже зарегистрирован в системе.'), code='duplicate')


def check_exist_username(username: str):
    if User.objects.filter(username__icontains=username).exists():
        raise ValidationError(_('Указанный логин уже зарегистрирован в системе.'), code='duplicate')
