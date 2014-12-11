import sys
from django.conf import settings

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
)

from django.test.runner import DiscoverRunner
test_runner = DiscoverRunner()
failures = test_runner.run_tests(['django_react'])
if failures:
    sys.exit(failures)