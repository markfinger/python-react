import os

SECRET_KEY = '_'

STATIC_URL = '/static/'

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'react',
    'tests.django_test_app',
)


TEST_ROOT = os.path.dirname(__file__)
COMPONENT_ROOT = os.path.join(TEST_ROOT, 'components')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
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