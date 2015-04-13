import os

# DJANGO
# ======

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True

TEMPLATE_DEBUG = DEBUG

SECRET_KEY = '_'

INSTALLED_APPS = (
    'django.contrib.staticfiles',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'djangosite', 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'djangosite', 'templates'),
)

MIDDLEWARE_CLASSES = ()

ROOT_URLCONF = 'djangosite.urls'

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# DJANGO NODE
# ===========

INSTALLED_APPS += (
    'django_node',
)

DJANGO_NODE = {
    'SERVICES': (),
    'PACKAGE_DEPENDENCIES': (),
}

# Instruct django-node to install the package.json dependencies
DJANGO_NODE['PACKAGE_DEPENDENCIES'] += (
    BASE_DIR,
)


# DJANGO WEBPACK
# ==============

INSTALLED_APPS += (
    'django_webpack',
)

DJANGO_NODE['SERVICES'] += (
    'django_webpack.services',
)

STATICFILES_FINDERS += (
    'django_webpack.staticfiles.WebpackFinder',
)

# DJANGO REACT
# ============

INSTALLED_APPS += (
    'django_react',
)

DJANGO_NODE['SERVICES'] += (
    'django_react.services',
)