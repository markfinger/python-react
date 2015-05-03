# Django-specific settings

DEBUG = True

SECRET_KEY = '_'

STATIC_URL = '/static/'

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'js_host',
    'webpack',
    'tests.django_test_app',
)

STATICFILES_FINDERS = (
    # Defaults
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # Webpack finder
    'webpack.django_integration.WebpackFinder',
)