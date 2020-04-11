from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ApiConfig(AppConfig):
    name = 'src.apps.api'
    label = 'api'

    def ready(self):
        self.verbose_name = _('API')
