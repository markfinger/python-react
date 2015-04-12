import os
import json
from django.contrib.staticfiles import finders
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
from .exceptions import ComponentSourceFileNotFound, ComponentWasNotBundled
from .services import RenderService
from .settings import WATCH_SOURCE
from .bundle import bundle_component

service = RenderService()


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
        return self.render_markup()

    def __unicode__(self):
        return self.render_markup()

    def render_markup(self):
        markup = self.markup
        if self.bundle and not self.to_static_markup:
            markup = '<span id="{id}">{markup}</span>'.format(
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
            raise ComponentWasNotBundled((
                'The component "{path}" was not bundled during the rendering process. '
                'Call render_component with `bundle`, `translate`, or `watch_source` '
                'keyword arguments set to `True` to ensure that it is bundled.'
            ).format(path=self.path_to_source))
        return self.bundle

    def get_var(self):
        return self.get_bundle().get_library()

    def get_container_id(self):
        return 'reactComponent-' + self.get_var()

    def get_props_var(self):
        return self.get_var() + '__props'

    def render_mount_js(self):
        mount_js = '''if (typeof React === 'undefined') throw new Error('Cannot find `React` global variable. Have you added a script element to this page which points to React?');
if (typeof {var} === 'undefined') throw new Error('Cannot find component variable `{var}`');
(function(React, component, containerId) {{
  var props = {props};
  var element = React.createElement(component, props);
  var container = document.getElementById(containerId);
  if (!container) throw new Error('Cannot find the container element `#{container_id}` for component `{var}`');
  React.render(element, container);
}})(React, {var}, '{container_id}');'''
        return mark_safe(
            mount_js.format(
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
        absolute_path_to_source = finders.find(path_to_source)
        if not absolute_path_to_source:
            raise ComponentSourceFileNotFound(path_to_source)
        path_to_source = absolute_path_to_source

    if not os.path.exists(path_to_source):
        raise ComponentSourceFileNotFound(path_to_source)

    bundled_component = None
    if bundle or translate or watch_source:
        bundled_component = bundle_component(path_to_source, translate=translate, watch=watch_source)
        path_to_source = bundled_component.get_assets()[0]['path']

    if watch_source is None:
        watch_source = WATCH_SOURCE

    if json_encoder is None:
        json_encoder = DjangoJSONEncoder

    if props is not None:
        serialized_props = json.dumps(props, cls=json_encoder)
    else:
        serialized_props = None

    markup = service.render(path_to_source, serialized_props, to_static_markup)

    return RenderedComponent(
        markup, path_to_source, props, serialized_props, watch_source, bundled_component, to_static_markup
    )