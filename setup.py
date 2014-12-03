from setuptools import setup

VERSION = '0.2.0'

setup(
    name='django-react',
    version=VERSION,
    packages=['django_react'],
    package_data={
        'django_react': [
            '*.js',
            '*.json',
        ]
    },
    install_requires=[
        'django',
        'django-node >= 0.1.0',
    ],
    description='Django React',
    long_description=open('README.md', 'rb').read().decode('utf-8'),
    author='Mark Finger',
    author_email='markfinger@gmail.com',
    url='https://github.com/markfinger/django-react',
)