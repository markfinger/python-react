import os

DEBUG = True

SECRET_KEY = '_'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static_root')

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'tests.test_app',
)

DJANGO_NODE = {
    'SERVICES': (
        'django_react.services',
        'django_webpack.services',
    )
}