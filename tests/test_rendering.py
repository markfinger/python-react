import os
from optional_django import six
from webpack.compiler import WebpackBundle
from react.render import render_component, RenderedComponent
from react.exceptions import ReactRenderingError, ComponentSourceFileNotFound, ComponentWasNotBundled
from .utils import BaseTest
from .settings import COMPONENT_ROOT


HELLO_WORLD_COMPONENT_JS = os.path.join(COMPONENT_ROOT, 'HelloWorld.js')
HELLO_WORLD_COMPONENT_JSX = os.path.join(COMPONENT_ROOT, 'HelloWorld.jsx')
HELLO_WORLD_WRAPPER_COMPONENT = os.path.join(COMPONENT_ROOT, 'HelloWorldWrapper.jsx')
ERROR_THROWING_COMPONENT = os.path.join(COMPONENT_ROOT, 'ErrorThrowingComponent.jsx')
SYNTAX_ERROR_COMPONENT = os.path.join(COMPONENT_ROOT, 'SyntaxErrorComponent.jsx')


class TestRendering(BaseTest):
    __test__ = True

    def test_can_render_a_component_in_js(self):
        component = render_component(HELLO_WORLD_COMPONENT_JS, to_static_markup=True)
        self.assertEqual(str(component), '<span>Hello </span>')

    def test_can_render_a_component_in_jsx(self):
        component = render_component(HELLO_WORLD_COMPONENT_JSX, translate=True, to_static_markup=True)
        self.assertEqual(str(component), '<span>Hello </span>')

    def test_can_render_a_component_requiring_another_component(self):
        component = render_component(
            HELLO_WORLD_WRAPPER_COMPONENT,
            props={
                'name': 'world!',
                'numbers': [1, 2, 3, 4, 5],
            },
            translate=True,
            to_static_markup=True
        )
        self.assertEqual(str(component), '<div><span>Hello world!</span><span>10, 20, 30, 40, 50</span></div>')

    def test_can_render_a_component_to_a_string_with_props(self):
        component = render_component(
            HELLO_WORLD_COMPONENT_JSX,
            {'name': 'world!'},
            translate=True,
        )
        markup = str(component)
        self.assertNotEqual(markup, '<span>Hello world!</span>')
        self.assertIn('Hello ', markup)
        self.assertIn('world!', markup)

    def test_render_component_returns_a_rendered_component(self):
        component = render_component(
            HELLO_WORLD_COMPONENT_JSX,
            props={
                'name': 'world!'
            },
            translate=True,
            to_static_markup=True,
        )
        self.assertIsInstance(component, RenderedComponent)
        self.assertEqual(component.markup, '<span>Hello world!</span>')
        self.assertEqual(component.markup, str(component))
        if six.PY2:
            self.assertEqual(component.markup, unicode(component))

    def test_can_get_a_components_serialized_props(self):
        component = render_component(
            HELLO_WORLD_COMPONENT_JSX,
            props={
                'name': 'world!',
            },
            translate=True,
        )
        self.assertEqual(component.props, {'name': 'world!'})
        self.assertEqual(component.serialized_props, '{"name": "world!"}')
        self.assertEqual(component.render_props(), '{"name": "world!"}')

    def test_component_js_rendering_errors_raise_an_exception(self):
        self.assertRaises(ReactRenderingError, render_component, ERROR_THROWING_COMPONENT)
        self.assertRaises(ReactRenderingError, render_component, ERROR_THROWING_COMPONENT, to_static_markup=True)

    def test_components_with_syntax_errors_raise_exceptions(self):
        self.assertRaises(ReactRenderingError, render_component, SYNTAX_ERROR_COMPONENT)
        self.assertRaises(ReactRenderingError, render_component, SYNTAX_ERROR_COMPONENT, to_static_markup=True)

    def test_unserializable_props_raise_an_exception(self):
        self.assertRaises(
            TypeError,
            render_component,
            HELLO_WORLD_COMPONENT_JSX,
            props={'name': lambda: None}
        )
        self.assertRaises(
            TypeError,
            render_component,
            HELLO_WORLD_COMPONENT_JSX,
            props={'name': self}
        )

    def test_missing_paths_throw_an_exception(self):
        self.assertRaises(ComponentSourceFileNotFound, render_component, '/path/to/nothing.jsx')
        # Ensure that relative paths are handled as well
        self.assertRaises(ComponentSourceFileNotFound, render_component, 'path/to/nothing.jsx')

    def test_rendered_components_which_are_bundled_have_access_to_their_bundle(self):
        bundled_component = render_component(HELLO_WORLD_COMPONENT_JS, to_static_markup=True)
        self.assertRaises(ComponentWasNotBundled, bundled_component.get_bundle)

        bundled_component = render_component(HELLO_WORLD_COMPONENT_JS, to_static_markup=True, bundle=True)
        self.assertIsInstance(bundled_component.get_bundle(), WebpackBundle)

        translated_component = render_component(HELLO_WORLD_COMPONENT_JS, to_static_markup=True, translate=True)
        self.assertIsInstance(translated_component.get_bundle(), WebpackBundle)

        watched_component = render_component(HELLO_WORLD_COMPONENT_JS, to_static_markup=True, watch_source=True)
        self.assertIsInstance(watched_component.get_bundle(), WebpackBundle)

    def test_bundled_components_can_get_access_to_their_variable(self):
        component = render_component(HELLO_WORLD_COMPONENT_JS, to_static_markup=True, bundle=True)
        self.assertEqual(component.get_var(), 'components__HelloWorld')

    def test_bundled_components_have_their_markup_wrapped_in_a_container(self):
        component = render_component(HELLO_WORLD_COMPONENT_JS, bundle=True)
        self.assertEqual(str(component), '<span id="reactComponent-components__HelloWorld">' + component.markup + '</span>')

    def test_bundled_components_can_render_mount_js(self):
        component = render_component(HELLO_WORLD_COMPONENT_JS, bundle=True)
        expected = \
"""
if (typeof React === 'undefined') throw new Error('Cannot find `React` global variable. Have you added a script element to this page which points to React?');
if (typeof components__HelloWorld === 'undefined') throw new Error('Cannot find component variable `components__HelloWorld`');
(function(React, component, containerId) {
  var props = null;
  var element = React.createElement(component, props);
  var container = document.getElementById(containerId);
  if (!container) throw new Error('Cannot find the container element `#reactComponent-components__HelloWorld` for component `components__HelloWorld`');
  React.render(element, container);
})(React, components__HelloWorld, 'reactComponent-components__HelloWorld');
"""
        self.assertEqual(component.render_mount_js(), expected)

    def test_bundled_components_can_render_mount_js_with_props(self):
        component = render_component(HELLO_WORLD_COMPONENT_JS, props={'name': 'world!'}, bundle=True)
        expected = \
"""
if (typeof React === 'undefined') throw new Error('Cannot find `React` global variable. Have you added a script element to this page which points to React?');
if (typeof components__HelloWorld === 'undefined') throw new Error('Cannot find component variable `components__HelloWorld`');
(function(React, component, containerId) {
  var props = {"name": "world!"};
  var element = React.createElement(component, props);
  var container = document.getElementById(containerId);
  if (!container) throw new Error('Cannot find the container element `#reactComponent-components__HelloWorld` for component `components__HelloWorld`');
  React.render(element, container);
})(React, components__HelloWorld, 'reactComponent-components__HelloWorld');
"""
        self.assertEqual(component.render_mount_js(), expected)

    def test_bundled_components_can_render_script_elements_with_the_bundle_and_mount_js(self):
        component = render_component(HELLO_WORLD_COMPONENT_JS, bundle=True)
        self.assertEqual(
            component.render_js(),
            '\n<script src="' + component.bundle.get_urls()[0] + '"></script>\n<script>\n' + component.render_mount_js() + '\n</script>\n',
        )