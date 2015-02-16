from django.conf import settings

setting_overrides = getattr(settings, 'DJANGO_REACT', {})

REACT_EXTERNAL = setting_overrides.get(
    'REACT_EXTERNAL',
    'window.React',
)

RENDERER = setting_overrides.get(
    'RENDERER',
    'django_react.renderer.render',
)

INVALIDATE_CACHE = setting_overrides.get(
    'INVALIDATE_CACHE',
    False
)
