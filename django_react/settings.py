from django.conf import settings

setting_overrides = getattr(settings, 'DJANGO_REACT', {})

RENDERER = setting_overrides.get(
    'RENDERER',
    'django_react.renderer.render',
)

INVALIDATE_CACHE = setting_overrides.get(
    'INVALIDATE_CACHE',
    False
)

REACT_EXTERNAL = setting_overrides.get(
    'REACT_EXTERNAL',
    'window.React',
)

NPM_INSTALL_ON_INIT = setting_overrides.get(
    'NPM_INSTALL_ON_INIT',
    True,
)
