from optional_django import conf
from optional_django.env import DJANGO_SETTINGS


class Conf(conf.Conf):
    django_namespace = 'DJANGO_REACT'

    DEV_TOOL = DJANGO_SETTINGS.DEBUG if DJANGO_SETTINGS else False
    WATCH_SOURCE = DJANGO_SETTINGS.DEBUG if DJANGO_SETTINGS else False

settings = Conf()