import os
import sys
import subprocess
from setuptools import setup
from distutils.spawn import find_executable

VERSION = '0.1.0'

# Ensure that we are in the same directory as setup.py
path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))


def npm_install(operate_in, return_to):
    """
    cd into `operate_in`
    call `npm install`
    cd into `return_to`
    """

    # Ensure that npm is available
    path_to_npm = find_executable('npm')
    if not path_to_npm:
        raise Exception('Missing dependency: npm cannot be found')

    path_to_operate_in = os.path.join(path, operate_in)

    print('Changing directory to %s\n' % path_to_operate_in)

    os.chdir(path_to_operate_in)

    cmd_to_run = ('npm', 'install')

    print('Running `npm install`\n')

    popen = subprocess.Popen(cmd_to_run, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    pipe = popen.communicate()

    std_out = pipe[0]
    std_err = pipe[1]

    if std_err:
        for line in std_err.splitlines():
            if line.startswith('npm WARN'):
                print(line)
            else:
                raise Exception(line)

    if std_out:
        print std_out

    os.chdir(os.path.join(path, return_to))

    print('Completed `npm install`\n')

setup(
    name='django-react',
    version=VERSION,
    packages=['django_react'],
    install_requires=['django'],
    description='Django React',
    long_description=open('README.md', 'rb').read().decode('utf-8'),
    author='Mark Finger',
    author_email='markfinger@gmail.com',
    url='https://github.com/markfinger/django-react',
)

# Kinda hacky to put it here, but pip doesn't seem to like running
# post-install tasks. Tried the following without success...
# http://stackoverflow.com/questions/1321270/how-to-extend-distutils-with-a-simple-post-install-script
npm_install(
    operate_in='django_react',
    return_to='../'
)
