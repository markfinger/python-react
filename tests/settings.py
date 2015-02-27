DEBUG = True

SECRET_KEY = '_'

STATIC_URL = '/static/'

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'tests.test_app',
)

DJANGO_NODE = {
    'SERVICES': (
        'django_react.services',
    )
}