from typing import Optional

from django.forms import Form


def get_form_errors(form: Form) -> dict:
    errors_list = [''.join(e) for e in form.errors.values()]
    return {'status': ";".join(errors_list)}


def get_base_domain(url: str) -> Optional[str]:
    # Standard python urlparse package does not work correctly.
    if not url or '.' not in url:
        return None

    base_url: str = url.lower()

    # remove protocol
    if '://' in base_url:
        base_url = base_url.split("://")[1]

    # remove part after domain and query params
    base_url = base_url.split('/')[0].split("?")[0]

    return base_url
