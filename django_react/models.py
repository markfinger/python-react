import os
import hashlib
import json
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders
from django_webpack.models import WebpackBundle
import exceptions
import react
import settings


class ReactBundle(WebpackBundle):
    loaders = (
        {'loader': 'jsx', 'test': '.jsx$'},
    )
    paths_to_loaders = (os.path.abspath(os.path.join(os.path.dirname(__file__), 'node_modules')),)
    externals = {
        # Rather than bundling React, we rely on a browser global
        'react': settings.REACT_EXTERNAL,
        'react/addons': settings.REACT_EXTERNAL,
    }


class ReactComponent(object):
    source = None
    props = {}
    variable = None
    props_variable = None
    serialized_props = None
    bundle = ReactBundle
    source_url = None

    def __init__(self, **kwargs):
        if self.__class__ is ReactComponent:
            raise exceptions.ReactComponentCalledDirectly('Components must inherit from ReactComponent')
        if not self.source:
            raise exceptions.ReactComponentMissingSourceAttribute(self)
        self.props = kwargs

    def render_to_string(self):
        rendered = react.render(
            path_to_source=self.get_path_to_source(),
            serialized_props=self.get_serialized_props(),
        )
        rendered = rendered.strip()
        return self.render_container(content=rendered)

    def render_to_static_markup(self):
        rendered = react.render(
            path_to_source=self.get_path_to_source(),
            serialized_props=self.get_serialized_props(),
            to_static_markup=True,
        )
        rendered = rendered.strip()
        return self.render_container(content=rendered)

    def render_js(self):
        return render_to_string('django_react/js.html', self.get_render_context(
            rendered_props=self.render_props(),
            rendered_source=self.render_source(),
            rendered_init=self.render_init(),
        ))

    def render_container(self, content=None):
        return render_to_string('django_react/container.html', self.get_render_context(
            content=content,
            container_id=self.get_container_id(),
            container_class_name=self.get_container_class_name(),
        ))

    def render_props(self):
        return render_to_string('django_react/props.html', self.get_render_context(
            props_variable=self.get_props_variable(),
            serialized_props=self.get_serialized_props(),
        ))

    def render_source(self):
        return render_to_string('django_react/source.html', self.get_render_context(
            source_url=self.get_source_url()
        ))

    def render_init(self):
        return render_to_string('django_react/init.html', self.get_render_context(
            REACT_EXTERNAL=settings.REACT_EXTERNAL,
            variable=self.get_variable(),
            props_variable=self.get_props_variable(),
            container_id=self.get_container_id(),
        ))

    def get_render_context(self, **kwargs):
        context = {
            'component': self,
        }
        context.update(kwargs)
        return context

    def get_source(self):
        return self.source

    def get_path_to_source(self):
        source = self.get_source()
        path_to_source = finders.find(source)
        if not path_to_source or not os.path.exists(path_to_source):
            raise exceptions.SourceFileNotFound(path_to_source)
        return path_to_source

    def get_props(self):
        return self.props

    def get_variable(self):
        if not self.variable:
            self.variable = self.__class__.__name__
        return self.variable

    def get_container_id(self):
        return 'reactComponentContainer-{id}'.format(
            id=unicode(id(self)),
        )

    def get_container_class_name(self):
        return 'reactComponentContainer reactComponentContainer--{variable}'.format(
            variable=self.get_variable(),
        )

    def get_serialized_props(self):
        if not self.serialized_props:
            # While rendering templates Django will silently ignore some types of exceptions,
            # so we need to intercept them and raise our own class of exception
            try:
                self.serialized_props = json.dumps(self.get_props())
            except (TypeError, AttributeError) as e:
                raise exceptions.PropSerializationError(e.__class__.__name__, *e.args)
        return self.serialized_props

    def get_props_variable(self):
        if not self.props_variable:
            serialized_props = self.get_serialized_props()
            md5 = hashlib.md5()
            md5.update(serialized_props)
            self.props_variable = '__propsFor{variable}_{hash}__'.format(
                variable=self.get_variable(),
                hash=md5.hexdigest(),
            )
        return self.props_variable

    def get_source_url(self):
        if not self.source_url:
            bundle = self.bundle(
                entry=self.get_source(),
                library=self.get_variable(),
            )
            # While rendering templates Django will silently ignore some types of exceptions,
            # so we need to intercept them and raise our own class of exception
            try:
                self.source_url = bundle.get_url()
            except (TypeError, AttributeError) as e:
                raise exceptions.ComponentBundlingError(e.__class__.__name__, *e.args)
        return self.source_url