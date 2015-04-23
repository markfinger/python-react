from optional_django import conf


class Conf(conf.Conf):
    django_namespace = 'REACT'

    DEV_TOOL = False
    WATCH_SOURCE_FILES = False

settings = Conf()