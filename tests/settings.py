import os
from js_host.conf import settings as js_host_settings
from webpack.conf import settings as webpack_settings

TEST_ROOT = os.path.dirname(__file__)
COMPONENT_ROOT = os.path.join(TEST_ROOT, 'components')

js_host_settings.configure(
    SOURCE_ROOT=TEST_ROOT,
    # Let the manager spin up an instance
    USE_MANAGER=True,
    # Ensure the host stops when the python process does
    ON_EXIT_STOP_MANAGED_HOSTS_AFTER=0,
)

webpack_settings.configure(
    BUNDLE_ROOT=os.path.join(os.path.dirname(__file__), '__BUNDLE_ROOT__'),
    BUNDLE_URL='/static/',
)