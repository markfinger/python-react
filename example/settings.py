import os
from service_host.conf import settings as service_host_settings
from webpack.conf import settings as webpack_settings
from react.conf import settings as react_settings

DEBUG = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

service_host_settings.configure(
    CACHE=not DEBUG,
    USE_MANAGER=DEBUG,
    SOURCE_ROOT=BASE_DIR,
)

webpack_settings.configure(
    # The root directory that webpack will place files into and infer urls from
    BUNDLE_ROOT=os.path.join(BASE_DIR, 'static'),

    # The root url that webpack will use to determine the urls to bundles
    BUNDLE_URL='/static/',
)

react_settings.configure(
    DEVTOOL='eval',
    WATCH_SOURCE_FILES=DEBUG,
)