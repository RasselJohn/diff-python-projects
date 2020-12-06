from typing import Callable, Any, Optional

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy


def set_permission_for_url(
        permission_func: Optional[Callable[..., Any]],
        func: Optional[Callable[..., Any]] = None,
        redirect_field_name: str = REDIRECT_FIELD_NAME,
        login_url: Optional[str] = None
) -> Optional[Callable[..., Any]]:
    """
      Decorator for views that checks that the user is logged in as user,
      redirecting to the Log in page if necessary.
      """
    actual_decorator = user_passes_test(
        permission_func,
        login_url=reverse_lazy('index'),
        redirect_field_name=redirect_field_name
    )

    if func:
        return actual_decorator(func)

    return actual_decorator


def user_only_request(*args, **kwargs) -> Optional[Callable[..., Any]]:
    return set_permission_for_url(lambda u: u.is_authenticated, *args, **kwargs)


def staff_only_request(*args, **kwargs) -> Optional[Callable[..., Any]]:
    return set_permission_for_url(lambda u: u.is_authenticated and u.is_staff, *args, **kwargs)
