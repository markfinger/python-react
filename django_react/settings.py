from django.conf import settings

setting_overrides = getattr(settings, 'DJANGO_REACT', {})

CACHE_RENDERED_HTML = setting_overrides.get(
    'CACHE_RENDERED_HTML',
    not settings.DEBUG,
)

WATCH_COMPONENT_SOURCE = setting_overrides.get(
    'WATCH_COMPONENT_SOURCE',
    settings.DEBUG,
)