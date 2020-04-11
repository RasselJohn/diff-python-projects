from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy


def user_only_request(func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                      login_url=None):
    """
    Decorator for views that checks that the user is logged in as user, redirecting
    to the Log in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=reverse_lazy('index'),
        redirect_field_name=redirect_field_name
    )
    if func:
        return actual_decorator(func)
    return actual_decorator


def staff_only_request(func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                       login_url=None):
    """
    Decorator for views that checks that the user is logged in as user, redirecting
    to the Log in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url=reverse_lazy('index'),
        redirect_field_name=redirect_field_name
    )
    if func:
        return actual_decorator(func)
    return actual_decorator
