import os
import json
from django.contrib.staticfiles import finders
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
from .exceptions import ComponentSourceFileNotFound
from .services import RenderService
from .settings import WATCH_SOURCE

service = RenderService()


class RenderedComponent(object):
    def __init__(self, output, path_to_source, props, serialized_props, watch_source):
        self.output = output
        self.path_to_source = path_to_source
        self.props = props
        self.serialized_props = serialized_props
        self.watch_source = watch_source

    def __str__(self):
        return mark_safe(self.output)

    def __unicode__(self):
        return mark_safe(self.output)

    def render_props(self):
        if self.serialized_props:
            return mark_safe(self.serialized_props)
        return ''


def render_component(path_to_source, props=None, to_static_markup=None, watch_source=None, json_encoder=None):
    if not os.path.isabs(path_to_source):
        absolute_path_to_source = finders.find(path_to_source)
        if not absolute_path_to_source:
            raise ComponentSourceFileNotFound(path_to_source)
        path_to_source = absolute_path_to_source

    if not os.path.exists(path_to_source):
        raise ComponentSourceFileNotFound(path_to_source)

    if watch_source is None:
        watch_source = WATCH_SOURCE

    if json_encoder is None:
        json_encoder = DjangoJSONEncoder

    if props is not None:
        serialized_props = json.dumps(props, cls=json_encoder)
    else:
        serialized_props = None

    output = service.render(path_to_source, serialized_props, to_static_markup, watch_source)

    return RenderedComponent(output, path_to_source, props, serialized_props, watch_source)