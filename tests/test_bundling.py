import os
from webpack.config_file import JS, ConfigFile
from react.render import render_component
from react.bundle import (
    generate_var_from_path, generate_config_for_component, js_path_join, split_path, generate_config_file,
    get_path_to_config_file, bundle_component
)
from .utils import BaseTest
from .settings import TEST_ROOT, Components


class TestBundling(BaseTest):
    __test__ = True

    def test_can_generate_a_var_from_a_path(self):
        self.assertEqual(generate_var_from_path('/foo/bar/woz.jsx'), 'bar__woz')
        self.assertEqual(generate_var_from_path('/foo-bar/woz.jsx'), 'foo_bar__woz')
        self.assertEqual(generate_var_from_path('/foo/ba +\\r/woz.jsx'), 'ba_r__woz')
        self.assertEqual(generate_var_from_path('foo/test/one/two/bar/a'), 'bar__a')
        self.assertEqual(generate_var_from_path('foo/test/one/two/bar/.a'), 'bar___a')

    def test_can_generate_js_literal_to_join_paths(self):
        js = js_path_join(Components.HELLO_WORLD_JS)
        self.assertIsInstance(js, JS)
        self.assertEqual(
            js.content,
            'path.join.apply(path, ["' + '", "'.join(split_path(Components.HELLO_WORLD_JS)) + '"])'
        )

    def validate_generated_config(self, config, path, translate=None, devtool=None):
        self.assertIsInstance(config['context'], JS)
        self.assertEqual(
            config['context'].content,
            'path.join.apply(path, ["' + '", "'.join(split_path(os.path.dirname(path))) + '"])'
        )

        self.assertEqual(
            config['entry'],
            './' + os.path.basename(path)
        )

        self.assertIsInstance(config['output']['path'], JS)
        self.assertEqual(
            config['output']['path'].content,
            'path.join.apply(path, ["[bundle_dir]", "components"])'
        )

        var = generate_var_from_path(path)

        self.assertEqual(
            config['output']['filename'],
            var + '-[hash].js'
        )

        self.assertEqual(
            config['output']['filename'],
            var + '-[hash].js'
        )

        self.assertEqual(
            config['output']['libraryTarget'],
            'umd'
        )

        self.assertEqual(
            config['output']['library'],
            var
        )

        self.assertEqual(config['externals'][0]['react']['commonjs2'], 'react',)
        self.assertEqual(config['externals'][0]['react']['root'], 'React')

        self.assertEqual(config['externals'][0]['react/addons']['commonjs2'], 'react')
        self.assertEqual(config['externals'][0]['react/addons']['root'], 'React')

        if devtool:
            self.assertEqual(config['devtool'], devtool)

        if translate:
            self.assertIsInstance(config['module']['loaders'][0]['test'], JS)
            self.assertEqual(config['module']['loaders'][0]['test'].content, '/.jsx?$/')

            self.assertIsInstance(config['module']['loaders'][0]['exclude'], JS)
            self.assertEqual(config['module']['loaders'][0]['exclude'].content, '/node_modules/')

            self.assertEqual(config['module']['loaders'][0]['loader'], 'babel-loader')

            node_modules = os.path.join(TEST_ROOT, 'node_modules')
            self.assertIsInstance(config['resolveLoader']['root'], JS)
            self.assertEqual(
                config['resolveLoader']['root'].content,
                'path.join.apply(path, ["' + '", "'.join(split_path(node_modules)) + '"])',
            )

    def test_can_generate_a_webpack_config_for_a_js_component(self):
        config = generate_config_for_component(Components.HELLO_WORLD_JS)
        self.validate_generated_config(config, Components.HELLO_WORLD_JS)

    def test_can_generate_a_webpack_config_for_a_js_component_with_a_devtool(self):
        config = generate_config_for_component(Components.HELLO_WORLD_JS, devtool='eval')
        self.validate_generated_config(config, Components.HELLO_WORLD_JS, devtool='eval')

    def test_can_generate_a_webpack_config_for_a_jsx_component(self):
        config = generate_config_for_component(Components.HELLO_WORLD_JSX, translate=True)
        self.validate_generated_config(config, Components.HELLO_WORLD_JSX, translate=True)

    def test_can_generate_a_webpack_config_for_a_jsx_component_with_a_devtool(self):
        config = generate_config_for_component(Components.HELLO_WORLD_JSX, translate=True, devtool='eval')
        self.validate_generated_config(config, Components.HELLO_WORLD_JSX, translate=True, devtool='eval')

    def test_can_generate_and_create_a_config_file(self):
        config = generate_config_for_component(Components.HELLO_WORLD_JS)

        config_file = generate_config_file(config)
        self.assertIsInstance(config_file, ConfigFile)

        self.assertIsInstance(config_file.content[0], JS)
        self.assertEqual(config_file.content[0].content, 'var path = require("path");\n')

        self.assertIsInstance(config_file.content[1], JS)
        self.assertEqual(config_file.content[1].content, 'module.exports = ')

        self.assertEqual(config_file.content[2], config)
        self.validate_generated_config(config_file.content[2], Components.HELLO_WORLD_JS)

        self.assertIsInstance(config_file.content[3], JS)
        self.assertEqual(config_file.content[3].content, ';')

    def test_can_get_a_path_to_a_config_file(self):
        config = generate_config_for_component(Components.HELLO_WORLD_JS)

        config_file = generate_config_file(config)

        path = get_path_to_config_file(config_file)

        self.assertEqual(config_file.generate_path_to_file(), path)

        self.assertTrue(os.path.exists(path))

        with open(path, 'r') as output_file:
            content = output_file.read()

        self.assertEqual(content, config_file.render())

    def test_can_bundle_a_js_component(self):
        bundle = bundle_component(Components.HELLO_WORLD_JS)
        asset = bundle.get_assets()[0]
        self.assertTrue(os.path.exists(asset['path']))
        with open(asset['path'], 'r') as asset_file:
            contents = asset_file.read()
            self.assertIn('// __WEBPACK_BUNDLE_TEST__', contents)

    def test_can_bundle_a_jsx_component(self):
        bundle = bundle_component(Components.HELLO_WORLD_JSX, translate=True)
        asset = bundle.get_assets()[0]
        self.assertTrue(os.path.exists(asset['path']))
        with open(asset['path'], 'r') as asset_file:
            contents = asset_file.read()
            self.assertIn('// __WEBPACK_TRANSLATE_BUNDLE_TEST__', contents)

    def test_can_render_a_bundled_js_component(self):
        bundle = bundle_component(Components.HELLO_WORLD_JS)
        asset = bundle.get_assets()[0]
        component = render_component(asset['path'], to_static_markup=True)
        self.assertEqual(str(component), '<span>Hello </span>')

    def test_can_render_a_bundled_jsx_component(self):
        bundle = bundle_component(Components.HELLO_WORLD_JSX, translate=True)
        asset = bundle.get_assets()[0]
        component = render_component(asset['path'], to_static_markup=True)
        self.assertEqual(str(component), '<span>Hello </span>')

    def test_can_pass_props_when_rendering_a_bundled_js_component(self):
        bundle = bundle_component(Components.HELLO_WORLD_JS)
        asset = bundle.get_assets()[0]
        component = render_component(asset['path'], props={'name': 'world!'}, to_static_markup=True)
        self.assertEqual(str(component), '<span>Hello world!</span>')

    def test_can_pass_props_when_rendering_a_bundled_jsx_component(self):
        bundle = bundle_component(Components.HELLO_WORLD_JSX, translate=True)
        asset = bundle.get_assets()[0]
        component = render_component(asset['path'], props={'name': 'world!'}, to_static_markup=True)
        self.assertEqual(
            str(component),
            '<span>Hello world!</span>'
        )

    def test_bundled_components_omit_react_and_react_addons(self):
        bundle = bundle_component(Components.REACT_ADDONS, translate=True)
        with open(bundle.get_assets()[0]['path'], 'r') as bundle_file:
            content = bundle_file.read()
        # A bit hacky, but seems to work
        self.assertNotIn('Facebook', content)