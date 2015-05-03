import os
import sys
import json
from optional_django import staticfiles
from optional_django.serializers import JSONEncoder
from optional_django.safestring import mark_safe
from optional_django import six
from js_host.function import Function
from js_host.exceptions import FunctionError
from .exceptions import ComponentSourceFileNotFound, ComponentWasNotBundled
from .conf import settings
from .bundle import bundle_component
from .templates import MOUNT_JS
from .exceptions import ReactRenderingError


class RenderedComponent(object):
    def __init__(self, markup, path_to_source, props, serialized_props, bundle, to_static_markup):
        self.markup = markup
        self.path_to_source = path_to_source
        self.props = props
        self.serialized_props = serialized_props
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
                    'The component "{path}" was not bundled during the rendering process. Call render_component '
                    'with `bundle` or `translate` keyword arguments set to `True` to ensure that it is bundled.'
                ).format(path=self.path_to_source)
            )
        return self.bundle

    def get_var(self):
        return self.get_bundle().get_var()

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
                bundle=self.get_bundle(),
                mount_js=self.render_mount_js(),
            )
        )


js_host_function = Function(settings.JS_HOST_FUNCTION)


def render_component(
    # Rendering options
    path, props=None, to_static_markup=None,
    # Bundling options
    bundle=None, translate=None,
    # Prop handling
    json_encoder=None
):
    if not os.path.isabs(path):
        abs_path = staticfiles.find(path)
        if not abs_path:
            raise ComponentSourceFileNotFound(path)
        path = abs_path

    if not os.path.exists(path):
        raise ComponentSourceFileNotFound(path)

    bundled_component = None
    if bundle or translate:
        bundled_component = bundle_component(path, translate=translate)
        path = bundled_component.get_paths()[0]

    if json_encoder is None:
        json_encoder = JSONEncoder

    if props is not None:
        serialized_props = json.dumps(props, cls=json_encoder)
    else:
        serialized_props = None

    try:
        markup = js_host_function.call(
            path=path,
            serializedProps=serialized_props,
            toStaticMarkup=to_static_markup
        )
    except FunctionError as e:
        raise six.reraise(ReactRenderingError, ReactRenderingError(*e.args), sys.exc_info()[2])

    return RenderedComponent(markup, path, props, serialized_props, bundled_component, to_static_markup)