import os
import json
from optional_django import staticfiles
from optional_django.serializers import JSONEncoder
from .exceptions import ComponentSourceFileNotFound, ReactRenderingError
from .server import server


class RenderedComponent(object):
    def __init__(self, markup, props):
        self.markup = markup
        self.props = props

    def __str__(self):
        return self.markup

    def __unicode__(self):
        return unicode(self.markup)


def render_component(path, props=None, to_static_markup=None, json_encoder=None):
    if not os.path.isabs(path):
        abs_path = staticfiles.find(path)
        if not abs_path:
            raise ComponentSourceFileNotFound(path)
        path = abs_path

    if not os.path.exists(path):
        raise ComponentSourceFileNotFound(path)

    if json_encoder is None:
        json_encoder = JSONEncoder

    if props is not None:
        serialized_props = json.dumps(props, cls=json_encoder)
    else:
        serialized_props = None

    obj = server.render({
        'path': path,
        'serializedProps': serialized_props,
        'toStaticMarkup': to_static_markup
    })

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

    return RenderedComponent(markup, serialized_props)