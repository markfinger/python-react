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