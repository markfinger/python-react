import unittest
from optional_django import six
import mock
from react.conf import Conf
from react import render_server
from react.render import render_component
from react.render_server import RenderedComponent
from react.exceptions import ReactRenderingError, ComponentSourceFileNotFound
from .settings import Components
import json


class TestRendering(unittest.TestCase):
    __test__ = True

    def test_can_render_a_component_in_js(self):
        component = render_component(Components.HELLO_WORLD_JS, to_static_markup=True)
        self.assertEqual(str(component), '<span>Hello </span>')

    def test_can_render_a_component_in_jsx(self):
        component = render_component(Components.HELLO_WORLD_JSX, to_static_markup=True)
        self.assertEqual(str(component), '<span>Hello </span>')

    def test_can_render_a_component_requiring_another_component(self):
        component = render_component(
            Components.HELLO_WORLD_JSX_WRAPPER,
            {
                'name': 'world!',
                'numbers': [1, 2, 3, 4, 5],
            },
            to_static_markup=True
        )
        self.assertEqual(str(component), '<div><span>Hello world!</span><span>10, 20, 30, 40, 50</span></div>')

    def test_can_render_a_component_to_a_string_with_props(self):
        component = render_component(
            Components.HELLO_WORLD_JSX,
            {'name': 'world!'},
        )
        markup = str(component)
        self.assertNotEqual(markup, '<span>Hello world!</span>')
        self.assertIn('Hello ', markup)
        self.assertIn('world!', markup)

    def test_render_component_returns_a_rendered_component(self):
        component = render_component(
            Components.HELLO_WORLD_JSX,
            {
                'name': 'world!'
            },
            to_static_markup=True,
        )
        self.assertIsInstance(component, RenderedComponent)
        self.assertEqual(component.markup, '<span>Hello world!</span>')
        self.assertEqual(component.markup, str(component))
        if six.PY2:
            self.assertEqual(component.markup, unicode(component))

    def test_can_get_a_components_serialized_props(self):
        component = render_component(
            Components.HELLO_WORLD_JSX,
            {
                'name': 'world!',
            },
        )
        self.assertEqual(component.props, '{"name": "world!"}')

    def test_component_js_rendering_errors_raise_an_exception(self):
        self.assertRaises(ReactRenderingError, render_component, Components.ERROR_THROWING)
        self.assertRaises(ReactRenderingError, render_component, Components.ERROR_THROWING, to_static_markup=True)

    def test_components_with_syntax_errors_raise_exceptions(self):
        self.assertRaises(ReactRenderingError, render_component, Components.SYNTAX_ERROR)
        self.assertRaises(ReactRenderingError, render_component, Components.SYNTAX_ERROR, to_static_markup=True)

    def test_unserializable_props_raise_an_exception(self):
        self.assertRaises(
            TypeError,
            render_component,
            Components.HELLO_WORLD_JSX,
            {'name': lambda: None}
        )
        self.assertRaises(
            TypeError,
            render_component,
            Components.HELLO_WORLD_JSX,
            {'name': self}
        )

    def test_missing_paths_throw_an_exception(self):
        self.assertRaises(ComponentSourceFileNotFound, render_component, '/path/to/nothing.jsx')
        # Ensure that relative paths are handled as well
        self.assertRaises(ComponentSourceFileNotFound, render_component, 'path/to/nothing.jsx')

    def test_render_setting_is_respected(self):
        mock_settings = Conf()
        mock_settings.configure(RENDER=False)
        with mock.patch('react.conf.settings', mock_settings):
            rendered = render_component(
                Components.HELLO_WORLD_JSX,
                {'name': 'world!'},
                to_static_markup=True,
            )
            self.assertIsInstance(rendered, RenderedComponent)
            self.assertEqual(rendered.markup, '')
            self.assertEqual(str(rendered), '')
            self.assertEqual(rendered.props, '{"name": "world!"}')

    @mock.patch('requests.post')
    def test_can_pass_additional_request_headers(self, requests_post_mock):
        mock_json = {
            'markup': '<div>Hello</div>',
        }
        mock_url = 'http://localhost/render'

        response_mock = mock.Mock()
        response_mock.status_code = 200
        response_mock.text = json.dumps(mock_json)
        response_mock.json = mock.Mock(return_value=mock_json)
        requests_post_mock.return_value = response_mock

        mock_settings = Conf()
        mock_settings.configure(RENDER_URL=mock_url)
        with mock.patch('react.conf.settings', mock_settings):
            component = render_component(
                path=Components.HELLO_WORLD_JSX,
                props={'name': 'world!'},
                request_headers={
                    'Accept-language': 'fr-FR,en-US,en',
                },
            )

        requests_post_mock.assert_called_with(
            mock_url,
            data=mock.ANY,
            params=mock.ANY,
            headers={
                'content-type': 'application/json',
                'Accept-language': 'fr-FR,en-US,en',
            },
        )
