import json
import hashlib
import requests
from optional_django.serializers import JSONEncoder
from .exceptions import ReactRenderingError
from . import conf
from .exceptions import RenderServerError


class RenderedComponent(object):
    def __init__(self, markup, props):
        self.markup = markup
        self.props = props

    def __str__(self):
        return self.markup

    def __unicode__(self):
        return unicode(self.markup)


class RenderServer(object):
    def __init__(self, url):
        self.url = url

    def render(self, path, data=None, to_static_markup=False):
        if data is not None:
            props = json.dumps(data, cls=JSONEncoder)
        else:
            props = None

        if not conf.settings.RENDER:
            return RenderedComponent('', props)

        options = {
            'path': path,
            'serializedProps': props,
            'toStaticMarkup': to_static_markup
        }
        serialized_options = json.dumps(options)
        options_hash = hashlib.sha1(serialized_options.encode('utf-8')).hexdigest()

        try:
            res = requests.post(
                self.url,
                data=serialized_options,
                headers={'content-type': 'application/json'},
                params={'hash': options_hash}
            )
        except requests.ConnectionError:
            raise RenderServerError('Could not connect to render server at {}'.format(self.url))

        if res.status_code != 200:
            raise RenderServerError(
                'Unexpected response from render server at {} - {}: {}'.format(self.url, res.status_code, res.text)
            )

        obj = res.json()

        markup = obj.get('markup', None)
        err = obj.get('error', None)

        if err:
            if 'message' in err and 'stack' in err:
                raise ReactRenderingError(
                    'Message: {}\n\nStack trace: {}'.format(err['message'], err['stack'])
                )
            raise ReactRenderingError(err)

        if markup is None:
            raise ReactRenderingError('Render server failed to return markup. Returned: {}'.format(obj))

        return RenderedComponent(markup, props)


render_server = RenderServer(conf.settings.RENDER_URL)
