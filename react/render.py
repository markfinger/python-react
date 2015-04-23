import os
import sys
import json
from optional_django import staticfiles
from optional_django.serializers import JSONEncoder
from optional_django.safestring import mark_safe
from optional_django import six
from service_host.service import Service
from service_host.exceptions import ServiceError
from .exceptions import ComponentSourceFileNotFound, ComponentWasNotBundled
from .conf import settings
from .bundle import bundle_component
from .templates import MOUNT_JS
from .exceptions import ReactRenderingError

service = Service('react')


class RenderedComponent(object):
    def __init__(self, markup, path_to_source, props, serialized_props, watch_source, bundle, to_static_markup):
        self.markup = markup
        self.path_to_source = path_to_source
        self.props = props
        self.serialized_props = serialized_props
        self.watch_source = watch_source
        self.bundle = bundle
        self.to_static_markup = to_static_markup

    def __str__(self):
        return mark_safe(self.render_markup())

    def __unicode__(self):
        return mark_safe(unicode(self.render_markup()))

    def render_markup(self):
        markup = self.markup
        if self.bundle and not self.to_static_markup:
            template = '<span id="{id}">{markup}</span>'
            if six.PY2:
                template = unicode(template)
            markup = template.format(
                id=self.get_container_id(),
                markup=markup,
            )
        return mark_safe(markup)

    def render_props(self):
        if self.serialized_props:
            return mark_safe(self.serialized_props)
        return ''

    def get_bundle(self):
        if not self.bundle:
            raise ComponentWasNotBundled(
                (
                    'The component "{path}" was not bundled during the rendering process. '
                    'Call render_component with `bundle`, `translate`, or `watch_source` '
                    'keyword arguments set to `True` to ensure that it is bundled.'
                ).format(path=self.path_to_source)
            )
        return self.bundle

    def get_var(self):
        return self.get_bundle().get_library()

    def get_container_id(self):
        return 'reactComponent-' + self.get_var()

    def render_mount_js(self):
        return mark_safe(
            MOUNT_JS.format(
                var=self.get_var(),
                props=self.serialized_props or 'null',
                container_id=self.get_container_id()
            )
        )

    def render_js(self):
        return mark_safe(
            '\n{bundle}\n<script>\n{mount_js}\n</script>\n'.format(
                bundle=self.get_bundle().render(),
                mount_js=self.render_mount_js(),
            )
        )


def render_component(
    # Rendering options
    path_to_source, props=None, to_static_markup=None,
    # Bundling options
    bundle=None, translate=None, watch_source=None,
    # Prop handling
    json_encoder=None
):
    if not os.path.isabs(path_to_source):
        absolute_path_to_source = staticfiles.find(path_to_source)
        if not absolute_path_to_source:
            raise ComponentSourceFileNotFound(path_to_source)
        path_to_source = absolute_path_to_source

    if not os.path.exists(path_to_source):
        raise ComponentSourceFileNotFound(path_to_source)

    if watch_source is None:
        watch_source = settings.WATCH_SOURCE_FILES

    bundled_component = None
    if bundle or translate or watch_source:
        bundled_component = bundle_component(path_to_source, translate=translate, watch_source=watch_source)
        path_to_source = bundled_component.get_assets()[0]['path']

    if json_encoder is None:
        json_encoder = JSONEncoder

    if props is not None:
        serialized_props = json.dumps(props, cls=json_encoder)
    else:
        serialized_props = None

    try:
        res = service.call(
            path=path_to_source,
            serializedProps=serialized_props,
            toStaticMarkup=to_static_markup
        )
    except ServiceError as e:
        raise six.reraise(ReactRenderingError, ReactRenderingError(*e.args), sys.exc_info()[2])

    markup = res.text

    return RenderedComponent(
        markup, path_to_source, props, serialized_props, watch_source, bundled_component, to_static_markup
    )