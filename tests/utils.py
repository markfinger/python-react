import os
import shutil
import unittest
from js_host.host import host
from webpack.conf import settings as webpack_settings


class BaseTest(unittest.TestCase):
    """
    Between each test run, delete the bundle root and reset the server
    """

    __test__ = False

    @classmethod
    def setUpClass(cls):
        cls.clean_bundle_root()

    @classmethod
    def tearDownClass(cls):
        cls.clean_bundle_root()
        host.restart()

    @classmethod
    def clean_bundle_root(cls):
        # Clean out any files generated from previous test runs
        if os.path.exists(webpack_settings.BUNDLE_ROOT):
            shutil.rmtree(webpack_settings.BUNDLE_ROOT)