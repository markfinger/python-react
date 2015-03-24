from setuptools import setup

VERSION = '0.9.0'

setup(
    name='django-react',
    version=VERSION,
    packages=['django_react', 'django_react.services'],
    package_data={
        'django_react': [
            'package.json',
            'render_server.js',
            'renderer.js',
            'templates/django_react/*.html',
        ]
    },
    install_requires=[
        'django',
        'django-node==3.0.0',
        'django-webpack==2.1.2',
    ],
    description='Render and bundle React components from a Django application',
    long_description='Documentation at https://github.com/markfinger/django-react',
    author='Mark Finger',
    author_email='markfinger@gmail.com',
    url='https://github.com/markfinger/django-react',
)
