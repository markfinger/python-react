from django.conf import settings
from django.apps import AppConfig
import react.conf


class ReactConfig(AppConfig):
    name = 'react'

    def ready(self):
        react.conf.settings.configure(
            **getattr(settings, 'REACT', {})
        )