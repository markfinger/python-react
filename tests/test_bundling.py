import os
from react.render import render_component
from react.bundle import get_webpack_config, get_var_from_path, get_component_config_filename, bundle_component
from .utils import BaseTest
from .settings import TEST_ROOT, COMPONENT_ROOT


HELLO_WORLD_COMPONENT_JS = os.path.join(COMPONENT_ROOT, 'HelloWorld.js')
HELLO_WORLD_COMPONENT_JSX = os.path.join(COMPONENT_ROOT, 'HelloWorld.jsx')
REACT_ADDONS_COMPONENT = os.path.join(COMPONENT_ROOT, 'ReactAddonsComponent.jsx')


class TestBundling(BaseTest):
    __test__ = True

    def test_can_generate_a_var_from_a_path(self):
        self.assertEqual(get_var_from_path('/foo/bar/woz.jsx'), 'bar__woz')
        self.assertEqual(get_var_from_path('/foo-bar/woz.jsx'), 'foo_bar__woz')
        self.assertEqual(get_var_from_path('/foo/ba +\\r/woz.jsx'), 'ba_r__woz')
        self.assertEqual(get_var_from_path('foo/test/one/two/bar/a'), 'bar__a')
        self.assertEqual(get_var_from_path('foo/test/one/two/bar/.a'), 'bar___a')

    def test_can_generate_a_webpack_config_for_a_js_component(self):
        config = get_webpack_config(HELLO_WORLD_COMPONENT_JS)
        expected = \
"""
module.exports = {
    context: '%s',
    entry: './HelloWorld.js',
    output: {
        path: '[bundle_dir]/react-components',
        filename: 'components__HelloWorld-[hash].js',
        libraryTarget: 'umd',
        library: 'components__HelloWorld'
    },
    externals: [{
      react: {
        commonjs2: '%s',
        root: 'React'
      },
      'react/addons': {
        commonjs2: '%s',
        root: 'React'
      }
    }]
};
""" % (
    COMPONENT_ROOT,
    os.path.join(TEST_ROOT, 'node_modules', 'react'),
    os.path.join(TEST_ROOT, 'node_modules', 'react'),
)
        self.assertEqual(config, expected)

    def test_can_generate_a_webpack_config_for_a_js_component_with_a_devtool(self):
        config = get_webpack_config(HELLO_WORLD_COMPONENT_JS, devtool='eval')
        expected = \
"""
module.exports = {
    context: '%s',
    entry: './HelloWorld.js',
    output: {
        path: '[bundle_dir]/react-components',
        filename: 'components__HelloWorld-[hash].js',
        libraryTarget: 'umd',
        library: 'components__HelloWorld'
    },
    externals: [{
      react: {
        commonjs2: '%s',
        root: 'React'
      },
      'react/addons': {
        commonjs2: '%s',
        root: 'React'
      }
    }],
    devtool: 'eval'
};
""" % (
    COMPONENT_ROOT,
    os.path.join(TEST_ROOT, 'node_modules', 'react'),
    os.path.join(TEST_ROOT, 'node_modules', 'react'),
)
        self.assertEqual(config, expected)

    def test_can_generate_a_webpack_config_with_a_path_to_react(self):
        config = get_webpack_config(HELLO_WORLD_COMPONENT_JS, path_to_react='/abs/path/to/node_modules/react')
        expected = \
"""
module.exports = {
    context: '%s',
    entry: './HelloWorld.js',
    output: {
        path: '[bundle_dir]/react-components',
        filename: 'components__HelloWorld-[hash].js',
        libraryTarget: 'umd',
        library: 'components__HelloWorld'
    },
    externals: [{
      react: {
        commonjs2: '/abs/path/to/node_modules/react',
        root: 'React'
      },
      'react/addons': {
        commonjs2: '/abs/path/to/node_modules/react',
        root: 'React'
      }
    }]
};
""" % (
    COMPONENT_ROOT
)
        self.assertEqual(config, expected)

    def test_can_generate_a_webpack_config_for_a_jsx_component(self):
        config = get_webpack_config(HELLO_WORLD_COMPONENT_JSX, translate=True)
        expected = \
"""
module.exports = {
    context: '%s',
    entry: './HelloWorld.jsx',
    output: {
        path: '[bundle_dir]/react-components',
        filename: 'components__HelloWorld-[hash].js',
        libraryTarget: 'umd',
        library: 'components__HelloWorld'
    },
    externals: [{
      react: {
        commonjs2: '%s',
        root: 'React'
      },
      'react/addons': {
        commonjs2: '%s',
        root: 'React'
      }
    }],
    module: {
        loaders: [{
            test: /\.jsx$/,
            exclude: /node_modules/,
            loader: 'babel-loader'
        }]
    },
    resolveLoader: {
        root: '%s'
    }

};
""" % (
    COMPONENT_ROOT,
    os.path.join(TEST_ROOT, 'node_modules', 'react'),
    os.path.join(TEST_ROOT, 'node_modules', 'react'),
    os.path.join(TEST_ROOT, 'node_modules'),
)
        self.assertEqual(config, expected)

    def test_can_generate_a_webpack_config_for_a_jsx_component_with_a_devtool(self):
        config = get_webpack_config(HELLO_WORLD_COMPONENT_JSX, translate=True, devtool='eval')
        expected = \
"""
module.exports = {
    context: '%s',
    entry: './HelloWorld.jsx',
    output: {
        path: '[bundle_dir]/react-components',
        filename: 'components__HelloWorld-[hash].js',
        libraryTarget: 'umd',
        library: 'components__HelloWorld'
    },
    externals: [{
      react: {
        commonjs2: '%s',
        root: 'React'
      },
      'react/addons': {
        commonjs2: '%s',
        root: 'React'
      }
    }],
    devtool: 'eval',
    module: {
        loaders: [{
            test: /\.jsx$/,
            exclude: /node_modules/,
            loader: 'babel-loader'
        }]
    },
    resolveLoader: {
        root: '%s'
    }

};
""" % (
    COMPONENT_ROOT,
    os.path.join(TEST_ROOT, 'node_modules', 'react'),
    os.path.join(TEST_ROOT, 'node_modules', 'react'),
    os.path.join(TEST_ROOT, 'node_modules'),
)
        self.assertEqual(config, expected)

    def test_can_generate_and_create_a_config_file(self):
        filename = get_component_config_filename(HELLO_WORLD_COMPONENT_JS)
        with open(filename, 'r') as config_file:
            contents = config_file.read()
            self.assertEqual(contents, get_webpack_config(HELLO_WORLD_COMPONENT_JS))

        filename = get_component_config_filename(HELLO_WORLD_COMPONENT_JSX, translate=True)
        with open(filename, 'r') as config_file:
            contents = config_file.read()
            self.assertEqual(contents, get_webpack_config(HELLO_WORLD_COMPONENT_JSX, translate=True))

    def test_generated_config_files_are_cached(self):
        self.assertEqual(
            get_component_config_filename(HELLO_WORLD_COMPONENT_JS),
            get_component_config_filename(HELLO_WORLD_COMPONENT_JS),
        )
        self.assertEqual(
            get_component_config_filename(HELLO_WORLD_COMPONENT_JS, translate=True),
            get_component_config_filename(HELLO_WORLD_COMPONENT_JS, translate=True),
        )
        self.assertNotEqual(
            get_component_config_filename(HELLO_WORLD_COMPONENT_JS, translate=True),
            get_component_config_filename(HELLO_WORLD_COMPONENT_JS, translate=False),
        )
        self.assertNotEqual(
            get_component_config_filename(HELLO_WORLD_COMPONENT_JS),
            get_component_config_filename(HELLO_WORLD_COMPONENT_JSX),
        )
        self.assertNotEqual(
            get_component_config_filename(HELLO_WORLD_COMPONENT_JS, translate=True),
            get_component_config_filename(HELLO_WORLD_COMPONENT_JSX, translate=True),
        )
        self.assertNotEqual(
            get_component_config_filename(HELLO_WORLD_COMPONENT_JS, translate=True),
            get_component_config_filename(HELLO_WORLD_COMPONENT_JSX, translate=False),
        )
        self.assertNotEqual(
            get_component_config_filename(HELLO_WORLD_COMPONENT_JS, translate=False),
            get_component_config_filename(HELLO_WORLD_COMPONENT_JSX, translate=False),
        )

    def test_can_bundle_a_js_component(self):
        bundle = bundle_component(HELLO_WORLD_COMPONENT_JS)
        asset = bundle.get_assets()[0]
        self.assertTrue(os.path.exists(asset['path']))
        with open(asset['path'], 'r') as asset_file:
            contents = asset_file.read()
            self.assertIn('// __WEBPACK_BUNDLE_TEST__', contents)

    def test_can_bundle_a_jsx_component(self):
        bundle = bundle_component(HELLO_WORLD_COMPONENT_JSX, translate=True)
        asset = bundle.get_assets()[0]
        self.assertTrue(os.path.exists(asset['path']))
        with open(asset['path'], 'r') as asset_file:
            contents = asset_file.read()
            self.assertIn('// __WEBPACK_TRANSLATE_BUNDLE_TEST__', contents)

    def test_can_render_a_bundled_js_component(self):
        bundle = bundle_component(HELLO_WORLD_COMPONENT_JS)
        asset = bundle.get_assets()[0]
        component = render_component(asset['path'], to_static_markup=True)
        self.assertEqual(str(component), '<span>Hello </span>')

    def test_can_render_a_bundled_jsx_component(self):
        bundle = bundle_component(HELLO_WORLD_COMPONENT_JSX, translate=True)
        asset = bundle.get_assets()[0]
        component = render_component(asset['path'], to_static_markup=True)
        self.assertEqual(str(component), '<span>Hello </span>')

    def test_can_pass_props_when_rendering_a_bundled_js_component(self):
        bundle = bundle_component(HELLO_WORLD_COMPONENT_JS)
        asset = bundle.get_assets()[0]
        component = render_component(asset['path'], props={'name': 'world!'}, to_static_markup=True)
        self.assertEqual(str(component), '<span>Hello world!</span>')

    def test_can_pass_props_when_rendering_a_bundled_jsx_component(self):
        bundle = bundle_component(HELLO_WORLD_COMPONENT_JSX, translate=True)
        asset = bundle.get_assets()[0]
        component = render_component(asset['path'], props={'name': 'world!'}, to_static_markup=True)
        self.assertEqual(
            str(component),
            '<span>Hello world!</span>'
        )

    def test_bundled_components_omit_react_and_react_addons(self):
        bundle = bundle_component(REACT_ADDONS_COMPONENT, translate=True)
        with open(bundle.get_assets()[0]['path'], 'r') as bundle_file:
            content = bundle_file.read()
        # A bit hacky, but seems to work
        self.assertNotIn('Facebook, Inc', content)