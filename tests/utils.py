import os
import shutil
import unittest
from js_host.host import host
import webpack.conf


def clean_bundle_root():
    # Clean out any files generated from previous test runs
    if os.path.exists(webpack.conf.settings.BUNDLE_ROOT):
        shutil.rmtree(webpack.conf.settings.BUNDLE_ROOT)


class BaseTest(unittest.TestCase):
    """
    Between each test run, delete the bundle root and reset the server
    """

    __test__ = False

    @classmethod
    def setUpClass(cls):
        clean_bundle_root()

    @classmethod
    def tearDownClass(cls):
        clean_bundle_root()
        host.restart()