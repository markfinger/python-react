from optional_django import conf


class Conf(conf.Conf):
    # The devtool that webpack uses when bundling components
    DEVTOOL = None

    # The default import path used when rendering components
    PATH_TO_REACT = None

    JS_HOST_FUNCTION = 'react'

settings = Conf()