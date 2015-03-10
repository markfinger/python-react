import datetime
import json
import os
import unittest
from django.utils import timezone
from django_react.render import render_component, ReactComponent
from django_react.exceptions import RenderingError, PropSerializationError, SourceFileNotFound

COMPONENT_ROOT = os.path.join(os.path.dirname(__file__), 'components')
HELLO_WORLD_COMPONENT_JS = os.path.join(COMPONENT_ROOT, 'HelloWorld.js')
HELLO_WORLD_COMPONENT_JSX = os.path.join(COMPONENT_ROOT, 'HelloWorld.jsx')
HELLO_WORLD_WRAPPER_COMPONENT = os.path.join(COMPONENT_ROOT, 'HelloWorldWrapper.jsx')
ERROR_THROWING_COMPONENT = os.path.join(COMPONENT_ROOT, 'ErrorThrowingComponent.jsx')
SYNTAX_ERROR_COMPONENT = os.path.join(COMPONENT_ROOT, 'SyntaxErrorComponent.jsx')
STATIC_FILE_FINDER_COMPONENT = 'test_app/StaticFileFinderComponent.jsx'


class TestDjangoReact(unittest.TestCase):
    def test_can_render_a_component_in_js(self):
        rendered = render_component(HELLO_WORLD_COMPONENT_JSX, to_static_markup=True)
        self.assertEqual(rendered, '<span>Hello </span>')

    def test_can_render_a_component_in_jsx(self):
        rendered = render_component(HELLO_WORLD_COMPONENT_JSX, to_static_markup=True)
        self.assertEqual(rendered, '<span>Hello </span>')

    def test_can_render_a_component_with_props(self):
        rendered = render_component(
            HELLO_WORLD_COMPONENT_JSX,
            json.dumps({'name': 'world!'}),
            to_static_markup=True
        )
        self.assertEqual(rendered, '<span>Hello world!</span>')

    def test_can_render_a_component_requiring_another_component(self):
        rendered = render_component(
            HELLO_WORLD_WRAPPER_COMPONENT,
            json.dumps({
                'name': 'world!',
                'numbers': [1, 2, 3, 4, 5],
            }),
            to_static_markup=True
        )
        self.assertEqual(rendered, '<div><span>Hello world!</span><span>10, 20, 30, 40, 50</span></div>')

    def test_can_render_a_component_to_a_string_with_props(self):
        rendered = render_component(
            HELLO_WORLD_COMPONENT_JSX,
            json.dumps({'name': 'world!'}),
        )
        self.assertNotEqual(rendered, '<span>Hello world!</span>')
        self.assertIn('Hello ', rendered)
        self.assertIn('world!', rendered)
        
    def test_can_render_a_react_component(self):
        component = ReactComponent(
            HELLO_WORLD_COMPONENT_JSX,
            name='world!'
        )
        rendered = component.render_to_static_markup()
        self.assertEqual(rendered, '<span>Hello world!</span>')

    def test_can_get_a_components_serialized_props(self):
        component = ReactComponent(
            HELLO_WORLD_COMPONENT_JSX,
            name='world!'
        )
        self.assertEqual(component.props, {'name': 'world!'})
        self.assertEqual(component.get_serialized_props(), '{"name": "world!"}')

    def test_can_serialize_datetime_values_in_props(self):
        component = ReactComponent(
            HELLO_WORLD_COMPONENT_JSX,
            name='world!',
            datetime=datetime.datetime(2015, 1, 2, 3, 4, 5, tzinfo=timezone.utc),
            date=datetime.date(2015, 1, 2),
            time=datetime.time(3, 4, 5),
        )

        serialized = component.get_serialized_props()

        deserialized = json.loads(serialized)
        self.assertEqual(
            deserialized,
            {
                'name': 'world!',
                'datetime': '2015-01-02T03:04:05Z',
                'date': '2015-01-02',
                'time': '03:04:05',
            }
        )

    def test_component_js_rendering_errors_raise_an_exception(self):
        self.assertRaises(RenderingError, render_component, ERROR_THROWING_COMPONENT)
        self.assertRaises(RenderingError, render_component, ERROR_THROWING_COMPONENT, to_static_markup=True)

        component = ReactComponent(ERROR_THROWING_COMPONENT)
        self.assertRaises(RenderingError, component.render_to_string)
        self.assertRaises(RenderingError, component.render_to_static_markup)

    def test_components_with_syntax_errors_raise_exceptions(self):
        self.assertRaises(RenderingError, render_component, SYNTAX_ERROR_COMPONENT)
        self.assertRaises(RenderingError, render_component, SYNTAX_ERROR_COMPONENT, to_static_markup=True)

        component = ReactComponent(SYNTAX_ERROR_COMPONENT)
        self.assertRaises(RenderingError, component.render_to_static_markup)
        self.assertRaises(RenderingError, component.render_to_string)

    def test_unserializable_props_raise_an_exception(self):
        component = ReactComponent(HELLO_WORLD_COMPONENT_JSX, name=lambda: None,)
        self.assertRaises(PropSerializationError, component.get_serialized_props)

        component = ReactComponent(HELLO_WORLD_COMPONENT_JSX, name=self)
        self.assertRaises(PropSerializationError, component.get_serialized_props)

    def test_relative_paths_are_resolved_via_the_static_file_finder(self):
        rendered = render_component(STATIC_FILE_FINDER_COMPONENT, to_static_markup=True)
        self.assertEqual(rendered, '<span>You found me.</span>')

    def test_missing_paths_throw_an_exception(self):
        self.assertRaises(SourceFileNotFound, render_component, '/path/to/nothing.jsx')
        # Ensure that relative paths are handled as well
        self.assertRaises(SourceFileNotFound, render_component, 'path/to/nothing.jsx')