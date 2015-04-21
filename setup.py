from setuptools import setup
import django_react

setup(
    name='django-react',
    version=django_react.VERSION,
    packages=['django_react', 'django_react.services'],
    package_data={
        'django_react': [
            'services/package.json',
            'services/render.js',
        ]
    },
    install_requires=[
        'django-node==4.0.0',
        'django-webpack==3.1.0',
        'optional-django==0.2.1'
    ],
    description='Render and bundle React components from a Django application',
    long_description='Documentation at https://github.com/markfinger/django-react',
    author='Mark Finger',
    author_email='markfinger@gmail.com',
    url='https://github.com/markfinger/django-react',
)
