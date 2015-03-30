import os
import requests
from django.contrib.staticfiles import finders
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
from django.conf import settings
from .exceptions import ComponentSourceFileNotFound, ComponentRenderingError

SERVICE_URL = getattr(settings, 'REACT_SERVICE_URL', 'http://localhost:63578/render')


class RenderedComponent(object):
    def __init__(self, output, path_to_source, props, json_encoder):
        self.output = output
        self.path_to_source = path_to_source
        self.props = props
        self.json_encoder = json_encoder

    def __str__(self):
        return mark_safe(self.output)

    def __unicode__(self):
        return mark_safe(self.output)

    def render_props(self):
        if self.props:
            return mark_safe(self.json_encoder().encode(self.props))
        return '{}'


def render_component(path_to_source, props=None, to_static_markup=False, json_encoder=None):
    if not os.path.isabs(path_to_source):
        path_to_source = finders.find(path_to_source) or path_to_source

    if not os.path.exists(path_to_source):
        raise ComponentSourceFileNotFound(path_to_source)

    if json_encoder is None:
        json_encoder = DjangoJSONEncoder

    response = requests.post(SERVICE_URL,
        timeout=10.0,
        headers={'Content-Type': 'application/json'},
        data=json_encoder().encode({
            'props': props,
            'path_to_source': path_to_source,
            'to_static_markup': to_static_markup,
        }))

    if response.status_code != 200:
        raise ComponentRenderingError(response.text)

    return RenderedComponent(response.text, path_to_source, props, json_encoder)
