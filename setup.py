from setuptools import setup
import react

setup(
    name='react',
    version=react.__version__,
    packages=['react'],
    install_requires=[
        'requests>=2.5.0',
        'optional-django==0.3.0',
    ],
    description='Server-side rendering of React components with data from your Python system',
    long_description='Documentation at https://github.com/markfinger/python-react',
    author='Mark Finger',
    author_email='markfinger@gmail.com',
    url='https://github.com/markfinger/python-react',
)
