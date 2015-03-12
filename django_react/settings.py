from django.conf import settings

setting_overrides = getattr(settings, 'DJANGO_REACT', {})

WATCH_SOURCE = setting_overrides.get(
    'WATCH_SOURCE',
    settings.DEBUG,
)