import os
from js_host.conf import settings as js_host_settings
from webpack.conf import settings as webpack_settings
from react.conf import settings as react_settings

DEBUG = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

js_host_settings.configure(
    # USE_MANAGER=DEBUG
)

webpack_settings.configure(
    # The root directory that webpack will place files into and infer urls from
    BUNDLE_ROOT=os.path.join(BASE_DIR, 'static'),

    # The root url that webpack will use to determine the urls to bundles
    BUNDLE_URL='/static/',

    WATCH_SOURCE_FILES=DEBUG,

    WATCH_CONFIG_FILES=DEBUG,
)

react_settings.configure(
    DEVTOOL='eval' if DEBUG else None,
)