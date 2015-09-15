class Conf(object):
    _render_url = 'http://127.0.0.1:9009/render'
    _render = True
    _PROXY_DJANGO_SETTINGS = False

    @property
    def RENDER_URL(self):
        if not self._PROXY_DJANGO_SETTINGS:
            return self._render_url

        from django.conf import settings

        if hasattr(settings, 'REACT'):
            return settings.REACT.get('RENDER_URL', self._render_url)

        return self._render_url

    @property
    def RENDER(self):
        if not self._PROXY_DJANGO_SETTINGS:
            return self._render

        from django.conf import settings

        if hasattr(settings, 'REACT'):
            return settings.REACT.get('RENDER', self._render)

        return self._render

    def configure(self, RENDER_URL=None, RENDER=None):
        if RENDER_URL is not None:
            self._render_url = RENDER_URL
        if RENDER is not None:
            self._render = RENDER

settings = Conf()
