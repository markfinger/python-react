from optional_django import conf


class Conf(conf.Conf):
    django_namespace = 'REACT'

    # The webpack devtool used by default when bundling components
    DEVTOOL = None

    # The default import path used when the service-host renders components
    PATH_TO_REACT = None

    # Indicates if webpack should watch your source files for changes when
    # bundling components
    WATCH_SOURCE_FILES = False

    FUNCTION_NAME = 'react'

settings = Conf()