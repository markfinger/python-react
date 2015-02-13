from django.conf import settings

setting_overrides = getattr(settings, 'DJANGO_REACT', {})

STATIC_ROOT = setting_overrides.get(
    'STATIC_ROOT',
    settings.STATIC_ROOT,
)

STATIC_URL = setting_overrides.get(
    'STATIC_URL',
    settings.STATIC_URL,
)

REACT_EXTERNAL = setting_overrides.get(
    'REACT_EXTERNAL',
    'window.React',
)

RENDERER = setting_overrides.get(
    'RENDERER',
    'django_react.render_service.render_service',
)