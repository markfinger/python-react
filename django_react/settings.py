import os
from django.conf import settings

setting_overrides = getattr(settings, 'DJANGO_REACT', {})

ENGINE = setting_overrides.get(
    'ENGINE',
    'node'
)

RENDERER = setting_overrides.get(
    'RENDERER',
    os.path.abspath(os.path.join(__file__, '../render.js'))
)

BUNDLER = setting_overrides.get(
    'BUNDLER',
    os.path.abspath(os.path.join(__file__, '../bundle.js'))
)

STATIC_ROOT = setting_overrides.get(
    'STATIC_ROOT',
    settings.STATIC_ROOT,
)

STATIC_URL = setting_overrides.get(
    'STATIC_URL',
    settings.STATIC_URL,
)