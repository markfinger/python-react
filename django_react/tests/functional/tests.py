import os
import unittest
import shutil
from django.conf import settings
from django.utils.safestring import mark_safe
from django_webpack.exceptions import BundlingError
from django_react import ReactComponent, ReactBundle, render_component
from django_react.exceptions import (
    RenderingError, PropSerializationError, ReactComponentCalledDirectly, ReactComponentMissingSource,
    SourceFileNotFound,
)
from django_react.settings import RENDERER

print('Running tests with DJANGO_REACT[\'RENDERER\'] = \'{renderer}\''.format(renderer=RENDERER))


class HelloWorld(ReactComponent):
    source = 'components/HelloWorld.jsx'


class HelloWorldJS(ReactComponent):
    source = 'components/HelloWorld.js'


class ErrorThrowingComponent(ReactComponent):
    source = 'components/ErrorThrowingComponent.jsx'


class SyntaxErrorComponent(ReactComponent):
    source = 'components/SyntaxErrorComponent.jsx'


class TestDjangoReact(unittest.TestCase):
    def tearDown(self):
        if os.path.exists(settings.STATIC_ROOT):
            shutil.rmtree(settings.STATIC_ROOT)

    def test_react_component_cannot_be_called_directly(self):
        self.assertRaises(ReactComponentCalledDirectly, ReactComponent)

    def test_react_component_requires_source_attribute(self):
        class ComponentMissingSourceAttribute(ReactComponent):
            pass
        self.assertRaises(ReactComponentMissingSource, ComponentMissingSourceAttribute)

        class ComponentWithNonExistentSource(ReactComponent):
            source = 'some/missing/file.js'
        self.assertRaises(ReactComponentMissingSource, ComponentWithNonExistentSource)

        class ComponentWithNonExistentPathToSource(ReactComponent):
            path_to_source = '/some/missing/file.js'
        component = ComponentWithNonExistentPathToSource()
        self.assertRaises(SourceFileNotFound, component.render_to_static_markup)

    def test_can_render_a_react_component_in_jsx(self):
        component = HelloWorld()
        rendered = component.render_to_static_markup()
        expected = component.render_container(
            content=mark_safe('<span>Hello </span>')
        )
        self.assertEqual(rendered, expected)

    def test_can_render_a_react_component_in_js(self):
        component = HelloWorldJS()
        rendered = component.render_to_static_markup()
        expected = component.render_container(
            content=mark_safe('<span>Hello </span>')
        )
        self.assertEqual(rendered, expected)

    def test_can_render_a_react_component_with_props(self):
        component = HelloWorld(text='world!')
        rendered = component.render_to_static_markup()
        expected = component.render_container(
            content=mark_safe('<span>Hello world!</span>')
        )
        self.assertEqual(rendered, expected)

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
        self.assertTrue(
            rendered.startswith('<script src="/static/components/HelloWorld-')
        )
        self.assertTrue(
            rendered.endswith('.js"></script>')
        )

    def test_can_override_a_components_source_url_generation(self):
        class TestComponent(HelloWorld):
            def get_url_to_source(self):
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

    def test_components_have_a_react_bundle(self):
        self.assertEqual(ReactComponent.bundle, ReactBundle)

    def test_render_component_has_similar_output_to_react_component_render_methods(self):
        component = HelloWorld()
        rendered = render_component(
            path_to_source=component.get_path_to_source(),
            to_static_markup=True
        )
        expected = component.render_to_static_markup(wrap=False)
        self.assertEqual(rendered, expected)

    def test_path_to_source_can_be_specified(self):
        class ComponentWithPathToSource(ReactComponent):
            path_to_source = os.path.join(
                os.path.dirname(__file__),
                'components/HelloWorld.jsx'
            )
        component = ComponentWithPathToSource()
        self.assertEqual(component.path_to_source, component.get_path_to_source())
        self.assertEqual(
            component.render_to_static_markup(wrap=False),
            HelloWorld().render_to_static_markup(wrap=False)
        )
