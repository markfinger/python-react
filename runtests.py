import os
import sys

import django


if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    if hasattr(django, 'setup'):  # Only compatible with Django >= 1.7
        django.setup()

    # For Django 1.6, need to import after setting DJANGO_SETTINGS_MODULE.
    from django.conf import settings
    from django.test.utils import get_runner

    from django_node import npm
    npm.install(os.path.join(os.path.dirname(__file__), 'tests'))

    if '--start-node-server' in sys.argv:
        from django_node.server import server
        server.start(blocking=True)
        sys.exit('Node server exited')

    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['tests'])
    sys.exit(bool(failures))