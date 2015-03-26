from setuptools import setup

VERSION = '0.10.0'

setup(
    name='django-react',
    version=VERSION,
    packages=['django_react'],
    install_requires=[
        'django>=1.6'
    ],
    description='Render and bundle React components from a Django application',
    long_description='Documentation at https://github.com/markfinger/django-react',
    author='Mark Finger',
    author_email='markfinger@gmail.com',
    url='https://github.com/markfinger/django-react',
)
