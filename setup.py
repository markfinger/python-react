from setuptools import setup

VERSION = '0.4.0'

setup(
    name='django-react',
    version=VERSION,
    packages=['django_react'],
    package_data={
        'django_react': [
            '*.js',
            '*.json',
            'tests/*.py',
        ]
    },
    install_requires=[
        'django',
        'django-node >= 0.2.0',
        'django-webpack >= 0.0.2',
    ],
    description='Django React',
    long_description=\
'''
Provides an interface for Django to render and bundle React components.

Documentation at https://github.com/markfinger/django-react
''',
    author='Mark Finger',
    author_email='markfinger@gmail.com',
    url='https://github.com/markfinger/django-react',
)