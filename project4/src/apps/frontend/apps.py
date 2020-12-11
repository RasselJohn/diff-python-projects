from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FrontendConfig(AppConfig):
    name = 'src.apps.frontend'
    label = 'frontend'

    def ready(self):
        self.verbose_name = _('Фронтенд')
