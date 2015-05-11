from optional_django import conf


class Conf(conf.Conf):
    # The devtool that webpack uses when bundling components
    DEVTOOL = None

    # The default import path used when rendering components
    PATH_TO_REACT = None

    # A JavaScript regex which is used to test if a file should have the babel
    # loader run over it
    TRANSLATE_TEST = None

    JS_HOST_FUNCTION = 'react'

settings = Conf()