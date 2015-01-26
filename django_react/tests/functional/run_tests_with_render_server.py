if __name__ == '__main__':
    import os
    import sys

    import django
    from django.conf import settings
    from django.test.utils import get_runner

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_react.tests.functional.settings.render_server_settings'
    django.setup()

    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['django_react'])

    sys.exit(bool(failures))