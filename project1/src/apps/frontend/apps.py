from django.apps import AppConfig
from django.utils.cache import set_response_etag
from django.utils.translation import gettext_lazy  as _


class FrontendConfig(AppConfig):
    name = 'src.apps.frontend'
    label = 'frontend'

    def ready(self) -> None:
        self.verbose_name = _('Фронтенд')
