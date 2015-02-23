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

DEBUG = setting_overrides.get(
    'DEBUG',
    settings.DEBUG,
)

RENDERER = setting_overrides.get(
    'RENDERER',
    'django_react.render_server.ReactRenderServer'
)

PATH_TO_RENDER_SERVER_SOURCE = setting_overrides.get(
    'PATH_TO_RENDER_SERVER_SOURCE',
    os.path.abspath(os.path.join(os.path.dirname(__file__), 'render_server.js')),
)

RENDER_SERVER_PROTOCOL = setting_overrides.get(
    'RENDER_SERVER_PROTOCOL',
    'http',
)

RENDER_SERVER_ADDRESS = setting_overrides.get(
    'RENDER_SERVER_ADDRESS',
    '127.0.0.1',
)

RENDER_SERVER_PORT = setting_overrides.get(
    'RENDER_SERVER_PORT',
    '0',
)

START_RENDER_SERVER_ON_INIT = setting_overrides.get(
    'START_RENDER_SERVER_ON_INIT',
    False,
)

SHUTDOWN_RENDER_SERVER_ON_EXIT = setting_overrides.get(
    'SHUTDOWN_RENDER_SERVER_ON_EXIT',
    True,
)

RENDER_SERVER_DEBUG = setting_overrides.get(
    'RENDER_SERVER_DEBUG',
    False,
)

RENDER_SERVER_TEST_ENDPOINT = setting_overrides.get(
    'RENDER_SERVER_TEST_ENDPOINT',
    '/',
)

RENDER_SERVER_TEST_EXPECTED_OUTPUT = setting_overrides.get(
    'RENDER_SERVER_TEST_EXPECTED_OUTPUT',
    'django-react render server',
)

RENDER_SERVER_RENDERING_ENDPOINT = setting_overrides.get(
    'RENDER_SERVER_RENDERING_ENDPOINT',
    '/render',
)

PATH_TO_RENDERER_SOURCE = setting_overrides.get(
    'PATH_TO_RENDERER_SOURCE',
    os.path.abspath(os.path.join(os.path.dirname(__file__), 'renderer.js'))
)

NPM_INSTALL_ON_INIT = setting_overrides.get(
    'NPM_INSTALL_ON_INIT',
    True,
)
