import os
from django.conf import settings
from django_node.settings import PATH_TO_NODE as DEFAULT_PATH_TO_NODE

setting_overrides = getattr(settings, 'DJANGO_REACT', {})

PATH_TO_NODE = setting_overrides.get(
    'PATH_TO_NODE',
    DEFAULT_PATH_TO_NODE
)

NODE_VERSION_REQUIRED = setting_overrides.get(
    'NODE_VERSION_REQUIRED',
    (0, 10, 0)
)

NPM_VERSION_REQUIRED = setting_overrides.get(
    'NPM_VERSION_REQUIRED',
    (1, 2, 0)
)

CHECK_DEPENDENCIES = setting_overrides.get(
    'CHECK_DEPENDENCIES',
    True
)

CHECK_PACKAGES = setting_overrides.get(
    'CHECK_PACKAGES',
    True
)

RENDERER = setting_overrides.get(
    'RENDERER',
    os.path.abspath(os.path.join(__file__, '../render.js'))
)

STATIC_ROOT = setting_overrides.get(
    'STATIC_ROOT',
    settings.STATIC_ROOT,
)

STATIC_URL = setting_overrides.get(
    'STATIC_URL',
    settings.STATIC_URL,
)