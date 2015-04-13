import os
import re
import tempfile
from django_webpack.compiler import webpack
from .templates import BUNDLE_CONFIG, BUNDLE_TRANSLATE_CONFIG

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
    if var is None:
        var = get_var_from_path(path)

    translate_config = ''
    if translate:
        # JSX + ES6/7 support
        translate_config += BUNDLE_TRANSLATE_CONFIG.format(
            ext=os.path.splitext(path)[-1],
            node_modules=os.path.join(os.path.dirname(__file__), 'services', 'node_modules')
        )

    return BUNDLE_CONFIG.format(
        path_to_resolve=os.path.join(os.path.dirname(__file__), 'services', 'node_modules', 'resolve'),
        dir=os.path.dirname(path),
        file='./' + os.path.basename(path),
        var=var,
        translate_config=translate_config
    )


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