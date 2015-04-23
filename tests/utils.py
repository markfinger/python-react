import os
import shutil
from webpack.conf import settings


def clean_bundle_root():
    # Clean out any files generated from previous test runs
    if os.path.exists(settings.BUNDLE_ROOT):
        shutil.rmtree(settings.BUNDLE_ROOT)