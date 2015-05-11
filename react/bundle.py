import json
import os
import re
import tempfile
from optional_django import staticfiles
from webpack.compiler import webpack
from webpack.config_file import ConfigFile, JS
from js_host.conf import settings as js_host_settings
from .exceptions import ComponentSourceFileNotFound
from .conf import settings


def bundle_component(path, translate=None, path_to_react=None, devtool=None):
    if not os.path.isabs(path):
        abs_path = staticfiles.find(path)
        if not abs_path:
            raise ComponentSourceFileNotFound(path)
        path = abs_path

    if not os.path.exists(path):
        raise ComponentSourceFileNotFound(path)

    config = generate_config_for_component(path, translate=translate, path_to_react=path_to_react, devtool=devtool)

    config_file = generate_config_file(config)

    var = generate_var_from_path(path)

    path_to_config_file = get_path_to_config_file(config_file, prefix=var + '.')

    return webpack(path_to_config_file)


def get_path_to_config_file(config_file, prefix=None):
    path = config_file.generate_path_to_file(prefix=prefix)
    return config_file.write(path, force=False)


def generate_config_file(config):
    return ConfigFile(
        JS('var path = require("path");\n'),
        JS('module.exports = '), config, JS(';'),
    )


def generate_config_for_component(path, translate=None, path_to_react=None, devtool=None):
    """
    Generates a webpack config object to bundle a component
    """

    var = generate_var_from_path(path)

    node_modules = os.path.join(js_host_settings.SOURCE_ROOT, 'node_modules')

    if path_to_react is None:
        path_to_react = settings.PATH_TO_REACT or os.path.join(node_modules, 'react')

    config = {
        'context': js_path_join(os.path.dirname(path)),
        'entry': '.' + os.path.sep + os.path.basename(path),
        'output': {
            'path': '[bundle_dir]/react-components',
            'filename': var + '-[hash].js',
            'libraryTarget': 'umd',
            'library': var
        },
        'externals': [{
            'react': {
                'commonjs2': js_path_join(path_to_react),
                'root': 'React'
            },
            'react/addons': {
                'commonjs2': js_path_join(path_to_react),
                'root': 'React'
            }
        }]
    }

    if translate:
        translate_test = settings.TRANSLATE_TEST or '/.jsx$/'

        config.update({
            'module': {
                'loaders': [{
                    'test': JS(translate_test),
                    'exclude': JS('/node_modules/'),
                    'loader': 'babel-loader'
                }]
            },
            'resolveLoader': {
                'root': js_path_join(node_modules)
            }
        })

    if devtool:
        config['devtool'] = devtool

    return config


def split_path(path):
    """
    Splits a path into the various parts and returns a list
    """

    parts = []

    drive, path = os.path.splitdrive(path)

    while True:
        newpath, tail = os.path.split(path)

        if newpath == path:
            assert not tail
            if path:
                parts.append(path)
            break

        parts.append(tail)
        path = newpath

    if drive:
        parts.append(drive)

    parts.reverse()

    return parts


def js_path_join(path):
    """
    Splits a path so that it can be rejoined by the JS engine. Helps to avoid
    OS compatibility issues due to string encoding
    """
    return JS('path.join.apply(path, ' + json.dumps(split_path(path)) + ')')


def generate_var_from_path(path):
    """
    Infer a variable name from a path
    """
    var = '{parent_dir}__{filename}'.format(
        parent_dir=os.path.basename(os.path.dirname(path)),
        filename=os.path.splitext(os.path.basename(path))[0]
    )
    return re.sub(r'\W+', '_', var)