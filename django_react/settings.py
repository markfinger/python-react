import os
from django.conf import settings

setting_overrides = getattr(settings, 'DJANGO_REACT', {})

NODE_VERSION_REQUIRED = setting_overrides.get(
    'NODE_VERSION_REQUIRED',
    (0, 10, 0)
)

NPM_VERSION_REQUIRED = setting_overrides.get(
    'NPM_VERSION_REQUIRED',
    (1, 2, 0)
)

PATH_TO_RENDERER = setting_overrides.get(
    'PATH_TO_RENDERER',
    os.path.abspath(os.path.join(os.path.dirname(__file__), 'render.js'))
)

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