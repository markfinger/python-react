import os
import re
import tempfile
from webpack.compiler import webpack
from js_host.conf import settings as js_host_settings
from .templates import BUNDLE_CONFIG, BUNDLE_TRANSLATE_CONFIG, DEVTOOL_CONFIG
from .conf import settings


def bundle_component(path, translate=None, path_to_react=None, devtool=None):
    filename = get_component_config_filename(path, translate=translate, path_to_react=path_to_react, devtool=devtool)
    return webpack(filename)

# TODO: replace this with a deterministic config file writer in webpack
COMPONENT_CONFIG_FILES = {}


def get_component_config_filename(path, translate=None, path_to_react=None, devtool=None):
    cache_key = (path, translate, path_to_react, devtool)
    if cache_key in COMPONENT_CONFIG_FILES:
        return COMPONENT_CONFIG_FILES[cache_key]

    config = get_webpack_config(path, translate=translate, path_to_react=path_to_react, devtool=devtool)
    filename = tempfile.mkstemp(suffix='.webpack.config.js')[1]
    with open(filename, 'w') as config_file:
        config_file.write(config)

    COMPONENT_CONFIG_FILES[cache_key] = filename

    return filename


def get_webpack_config(path, translate=None, path_to_react=None, devtool=None):
    if devtool is None:
        devtool = settings.DEVTOOL

    node_modules = os.path.join(js_host_settings.SOURCE_ROOT, 'node_modules')

    if path_to_react is None:
        path_to_react = settings.PATH_TO_REACT or os.path.join(node_modules, 'react')

    var = get_var_from_path(path)

    translate_config = ''
    if translate:
        # JSX + ES6/7 support
        translate_config += BUNDLE_TRANSLATE_CONFIG.format(
            ext=os.path.splitext(path)[-1],
            node_modules=node_modules
        )

    devtool_config = ''

    if devtool:
        devtool_config = DEVTOOL_CONFIG.format(devtool=devtool)

    return BUNDLE_CONFIG.format(
        path_to_react=path_to_react,
        dir=os.path.dirname(path),
        file='./' + os.path.basename(path),
        var=var,
        translate_config=translate_config,
        devtool_config=devtool_config,
    )


def get_var_from_path(path):
    var = '{parent_dir}__{filename}'.format(
        parent_dir=os.path.basename(os.path.dirname(path)),
        filename=os.path.splitext(os.path.basename(path))[0]
    )
    return re.sub(r'\W+', '_', var)