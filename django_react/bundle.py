import os
import re
import tempfile
from django_webpack.compiler import webpack
from .templates import BUNDLE_CONFIG, BUNDLE_TRANSLATE_CONFIG, DEV_TOOL_CONFIG
from .conf import settings

COMPONENT_CONFIG_FILES = {}

PATH_TO_NODE_MODULES = os.path.join(os.path.dirname(__file__), 'services', 'node_modules')


def bundle_component(path, translate=None, watch_source=None):
    filename = get_component_config_filename(path, translate)
    return webpack(filename, watch_source=watch_source)


def get_var_from_path(path):
    var = '{parent_dir}__{filename}'.format(
        parent_dir=os.path.basename(os.path.dirname(path)),
        filename=os.path.splitext(os.path.basename(path))[0]
    )
    return re.sub(r'\W+', '_', var)


def get_webpack_config(path, translate=None):
    var = get_var_from_path(path)

    translate_config = ''
    if translate:
        # JSX + ES6/7 support
        translate_config += BUNDLE_TRANSLATE_CONFIG.format(
            ext=os.path.splitext(path)[-1],
            node_modules=PATH_TO_NODE_MODULES
        )

    dev_tool_config = ''
    if settings.DEV_TOOL:
        dev_tool_config = DEV_TOOL_CONFIG

    return BUNDLE_CONFIG.format(
        path_to_resolve=os.path.join(PATH_TO_NODE_MODULES, 'resolve'),
        dir=os.path.dirname(path),
        file='./' + os.path.basename(path),
        var=var,
        translate_config=translate_config,
        dev_tool_config=dev_tool_config,
    )


def get_component_config_filename(path, translate=None):
    cache_key = (path, translate)
    if cache_key in COMPONENT_CONFIG_FILES:
        return COMPONENT_CONFIG_FILES[cache_key]

    config = get_webpack_config(path, translate)
    filename = tempfile.mkstemp(suffix='.webpack.config.js')[1]
    with open(filename, 'w') as config_file:
        config_file.write(config)

    COMPONENT_CONFIG_FILES[cache_key] = filename

    return filename