import datetime
import json
import os
import unittest
from django.utils import timezone, six
from django_react.render import render_component, RenderedComponent
from django_react.exceptions import ComponentRenderingError, ComponentSourceFileNotFound

COMPONENT_ROOT = os.path.join(os.path.dirname(__file__), 'components')

PATH_TO_HELLO_WORLD_COMPONENT_JS = os.path.join(COMPONENT_ROOT, 'HelloWorld.js')
PATH_TO_HELLO_WORLD_COMPONENT_JSX = os.path.join(COMPONENT_ROOT, 'HelloWorld.jsx')
PATH_TO_HELLO_WORLD_WRAPPER_COMPONENT = os.path.join(COMPONENT_ROOT, 'HelloWorldWrapper.jsx')
PATH_TO_ERROR_THROWING_COMPONENT = os.path.join(COMPONENT_ROOT, 'ErrorThrowingComponent.jsx')
PATH_TO_SYNTAX_ERROR_COMPONENT = os.path.join(COMPONENT_ROOT, 'SyntaxErrorComponent.jsx')
PATH_TO_STATIC_FILE_FINDER_COMPONENT = 'test_app/StaticFileFinderComponent.jsx'


class TestDjangoReact(unittest.TestCase):
    def test_can_render_a_component_in_js(self):
        component = render_component(PATH_TO_HELLO_WORLD_COMPONENT_JSX, to_static_markup=True)
        self.assertEqual(str(component), '<span>Hello </span>')

    def test_can_render_a_component_in_jsx(self):
        component = render_component(PATH_TO_HELLO_WORLD_COMPONENT_JSX, to_static_markup=True)
        self.assertEqual(str(component), '<span>Hello </span>')

    def test_can_render_a_component_with_props(self):
        component = render_component(
            PATH_TO_HELLO_WORLD_COMPONENT_JSX,
            props={'name': 'world!'},
            to_static_markup=True
        )
        self.assertEqual(str(component), '<span>Hello world!</span>')

    def test_can_render_a_component_requiring_another_component(self):
        component = render_component(
            PATH_TO_HELLO_WORLD_WRAPPER_COMPONENT,
            props={
                'name': 'world!',
                'numbers': [1, 2, 3, 4, 5],
            },
            to_static_markup=True
        )
        self.assertEqual(str(component), '<div><span>Hello world!</span><span>10, 20, 30, 40, 50</span></div>')

    def test_can_render_a_component_to_a_string_with_props(self):
        component = render_component(
            PATH_TO_HELLO_WORLD_COMPONENT_JSX,
            {'name': 'world!'},
        )
        markup = str(component)
        self.assertNotEqual(markup, '<span>Hello world!</span>')
        self.assertIn('Hello ', markup)
        self.assertIn('world!', markup)
        
    def test_render_component_returns_a_rendered_component(self):
        component = render_component(
            PATH_TO_HELLO_WORLD_COMPONENT_JSX,
            props={
                'name': 'world!'
            },
            to_static_markup=True,
        )
        self.assertIsInstance(component, RenderedComponent)
        self.assertEqual(component.output, '<span>Hello world!</span>')
        self.assertEqual(component.output, str(component))
        if six.PY2:
            self.assertEqual(component.output, unicode(component))

    def test_can_get_a_components_serialized_props(self):
        component = render_component(
            PATH_TO_HELLO_WORLD_COMPONENT_JSX,
            props={
                'name': 'world!',
            }
        )
        self.assertEqual(component.props, {'name': 'world!'})
        self.assertEqual(component.serialized_props, '{"name": "world!"}')
        self.assertEqual(component.render_props(), '{"name": "world!"}')

    def test_can_serialize_datetime_values_in_props(self):
        component = render_component(
            PATH_TO_HELLO_WORLD_COMPONENT_JSX,
            props={
                'name': 'world!',
                'datetime': datetime.datetime(2015, 1, 2, 3, 4, 5, tzinfo=timezone.utc),
                'date': datetime.date(2015, 1, 2),
                'time': datetime.time(3, 4, 5),
            }
        )
        deserialized = json.loads(component.serialized_props)
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
        self.assertRaises(ComponentRenderingError, render_component, PATH_TO_ERROR_THROWING_COMPONENT)
        self.assertRaises(ComponentRenderingError, render_component, PATH_TO_ERROR_THROWING_COMPONENT, to_static_markup=True)

    def test_components_with_syntax_errors_raise_exceptions(self):
        self.assertRaises(ComponentRenderingError, render_component, PATH_TO_SYNTAX_ERROR_COMPONENT)
        self.assertRaises(ComponentRenderingError, render_component, PATH_TO_SYNTAX_ERROR_COMPONENT, to_static_markup=True)

    def test_unserializable_props_raise_an_exception(self):
        self.assertRaises(
            TypeError,
            render_component,
            PATH_TO_HELLO_WORLD_COMPONENT_JSX,
            props={'name': lambda: None}
        )
        self.assertRaises(
            TypeError,
            render_component,
            PATH_TO_HELLO_WORLD_COMPONENT_JSX,
            props={'name': self}
        )

    def test_relative_paths_are_resolved_via_the_static_file_finder(self):
        component = render_component(PATH_TO_STATIC_FILE_FINDER_COMPONENT, to_static_markup=True)
        self.assertEqual(str(component), '<span>You found me.</span>')

    def test_missing_paths_throw_an_exception(self):
        self.assertRaises(ComponentSourceFileNotFound, render_component, '/path/to/nothing.jsx')
        # Ensure that relative paths are handled as well
        self.assertRaises(ComponentSourceFileNotFound, render_component, 'path/to/nothing.jsx')

    # TODO
    def test_component_source_is_watched_for_changes(self):
        pass