import os
import unittest
import shutil
from django.conf import settings
from django_webpack.exceptions import BundlingError
from django_react.models import ReactComponent
from django_react.exceptions import (
    RenderingError, PropSerializationError, ReactComponentCalledDirectly, ReactComponentMissingSourceAttribute,
)


class HelloWorld(ReactComponent):
    source = 'test_components/HelloWorld.jsx'


class HelloWorldJS(ReactComponent):
    source = 'test_components/HelloWorld.js'


class ErrorThrowingComponent(ReactComponent):
    source = 'test_components/ErrorThrowingComponent.jsx'


class SyntaxErrorComponent(ReactComponent):
    source = 'test_components/SyntaxErrorComponent.jsx'


class TestDjangoReact(unittest.TestCase):
    def tearDown(self):
        if os.path.exists(settings.STATIC_ROOT):
            shutil.rmtree(settings.STATIC_ROOT)

    def test_react_component_cannot_be_called_directly(self):
        self.assertRaises(ReactComponentCalledDirectly, ReactComponent)

    def test_react_component_requires_source_attribute(self):
        class ComponentMissingSource(ReactComponent):
            pass
        self.assertRaises(ReactComponentMissingSourceAttribute, ComponentMissingSource)

        class ComponentWithSourceAttribute(ReactComponent):
            source = 'some/file.js'
        ComponentWithSourceAttribute()

    def test_can_render_a_react_component_in_jsx(self):
        component = HelloWorld()
        rendered = component.render_to_static_markup()
        self.assertEqual(rendered, component.render_container(content='<span>Hello </span>'))

    def test_can_render_a_react_component_in_js(self):
        component = HelloWorldJS()
        rendered = component.render_to_static_markup()
        self.assertEqual(rendered, component.render_container(content='<span>Hello </span>'))

    def test_can_render_a_react_component_with_props(self):
        component = HelloWorld(text='world!')
        rendered = component.render_to_static_markup()
        self.assertEqual(rendered, component.render_container(content='<span>Hello world!</span>'))

    def test_can_render_a_react_component_container(self):
        component = HelloWorld()
        rendered = component.render_container()
        self.assertEqual(rendered, '<div id="{0}" class="{1}"></div>'.format(
            component.get_container_id(),
            component.get_container_class_name(),
        ))

    def test_can_render_a_react_source_element(self):
        component = HelloWorld()
        rendered = component.render_source()
        self.assertEqual(
            rendered,
            '<script src="/static/test_components/HelloWorld-9bcca9325027fdc7c693.js"></script>'
        )

    def test_can_override_a_components_source_url_generation(self):
        class TestComponent(HelloWorld):
            def get_source_url(self):
                return 'some/fake/file.js'
        component = TestComponent()
        rendered = component.render_source()
        self.assertEqual(
            rendered,
            '<script src="some/fake/file.js"></script>'
        )

    def test_component_js_rendering_errors_raise_an_exception(self):
        component = ErrorThrowingComponent()
        self.assertRaises(RenderingError, component.render_to_static_markup)
        self.assertRaises(RenderingError, component.render_to_string)

    def test_components_with_syntax_errors_raise_exceptions(self):
        component = SyntaxErrorComponent()
        self.assertRaises(RenderingError, component.render_to_static_markup)
        self.assertRaises(RenderingError, component.render_to_string)
        self.assertRaises(BundlingError, component.render_source)

    def test_unserializable_props_raise_an_exception(self):
        component = HelloWorld(text=id)
        self.assertRaises(PropSerializationError, component.get_serialized_props)
