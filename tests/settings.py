import os

TEST_ROOT = os.path.dirname(__file__)
COMPONENT_ROOT = os.path.join(TEST_ROOT, 'components')

SECRET_KEY = '_'

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(TEST_ROOT, 'static')

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'js_host',
    'webpack',
    'react',
    'tests.django_test_app',
)

STATICFILES_FINDERS = (
    # Defaults
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # Webpack finder
    'webpack.django_integration.WebpackFinder',
)

JS_HOST = {
    'SOURCE_ROOT': TEST_ROOT,
    # Let the manager spin up an instance
    'USE_MANAGER': True,
}

WEBPACK = {
    'BUNDLE_ROOT': STATIC_ROOT,
    'BUNDLE_URL': '/static/',
}


class Components(object):
    HELLO_WORLD_JS = os.path.join(COMPONENT_ROOT, 'HelloWorld.js')
    HELLO_WORLD_JSX = os.path.join(COMPONENT_ROOT, 'HelloWorld.jsx')
    REACT_ADDONS = os.path.join(COMPONENT_ROOT, 'ReactAddonsComponent.jsx')
    DJANGO_REL_PATH = 'django_test_app/StaticFileFinderComponent.jsx'
    PERF_TEST = os.path.join(COMPONENT_ROOT, 'PerfTestComponent.jsx')
    HELLO_WORLD_JSX_WRAPPER = os.path.join(COMPONENT_ROOT, 'HelloWorldWrapper.jsx')
    ERROR_THROWING = os.path.join(COMPONENT_ROOT, 'ErrorThrowingComponent.jsx')
    SYNTAX_ERROR = os.path.join(COMPONENT_ROOT, 'SyntaxErrorComponent.jsx')