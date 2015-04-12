import os
import re
import tempfile
from django_webpack.compiler import webpack

COMPONENT_CONFIG_FILES = {}


def bundle_component(path, translate=None, var=None, watch=None):
    filename = get_component_config_filename(path, translate, var)
    return webpack(filename)


def get_var_from_path(path):
    var = '{parent_dir}__{filename}'.format(
        parent_dir=os.path.basename(os.path.dirname(path)),
        filename=os.path.splitext(os.path.basename(path))[0]
    )
    return re.sub(r'\W+', '_', var)


def get_webpack_config(path, translate=None, var=None):
    config = 'module.exports = {'

    if var is None:
        var = get_var_from_path(path)

    config += '''
        context: '{dir}',
        entry: '{file}',
        output: {{
            path: '[bundle_dir]/components',
            filename: '{var}-[hash].js',
            libraryTarget: 'umd',
            library: '{var}'
        }},
        externals: ['react'],
        devtool: 'eval\''''.format(
        dir=os.path.dirname(path),
        file='./' + os.path.basename(path),
        var=var,
    )

    if translate:
        # JSX + ES6/7 support
        config += ''',
            module: {{
                loaders: [{{
                    test: /\{ext}$/,
                    exclude: /node_modules/,
                    loader: 'babel-loader'
                }}]
            }},
            resolveLoader: {{
                root: '{node_modules}'
            }}'''.format(
            ext=os.path.splitext(path)[-1],
            node_modules=os.path.join(os.path.dirname(__file__), 'services', 'node_modules')
        )

    return config + '\n};'


def get_component_config_filename(path, translate=None, var=None):
    cache_key = (path, translate, var)
    if cache_key in COMPONENT_CONFIG_FILES:
        return COMPONENT_CONFIG_FILES[cache_key]

    config = get_webpack_config(path, translate, var)
    filename = tempfile.mkstemp(suffix='.webpack.config.js')[1]
    with open(filename, 'w') as config_file:
        config_file.write(config)

    COMPONENT_CONFIG_FILES[cache_key] = filename

    return filename