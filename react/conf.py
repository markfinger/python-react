from optional_django import conf


class Conf(conf.Conf):
    RENDER_URL = 'http://127.0.0.1:9009/render'
    RENDER = True

settings = Conf()