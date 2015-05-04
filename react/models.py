# Django hook to configure settings on startup

from django.conf import settings
import react.conf

react.conf.settings.configure(
    **getattr(settings, 'REACT', {})
)