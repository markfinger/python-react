from optional_django import conf


class Conf(conf.Conf):
    django_namespace = 'REACT'

    # The devtool that webpack uses when bundling components
    DEVTOOL = None

    # The default import path used when the service-host renders components
    PATH_TO_REACT = None

    JS_HOST_FUNCTION = 'react'

settings = Conf()