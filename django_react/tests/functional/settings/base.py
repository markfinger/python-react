import os

DEBUG = True
INSTALLED_APPS = (
    'django_react',
)
TEST_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

SECRET_KEY = '_'
STATICFILES_DIRS = (
    TEST_ROOT_DIR,
)
STATIC_ROOT = os.path.abspath(os.path.join(TEST_ROOT_DIR, 'static'))
STATIC_URL = '/static/'