import os
import re
import tempfile
from webpack.compiler import webpack
from service_host.conf import settings as service_host_settings
from .templates import BUNDLE_CONFIG, BUNDLE_TRANSLATE_CONFIG, DEV_TOOL_CONFIG
from .conf import settings


def bundle_component(path, translate=None, watch_source_files=None):
    filename = get_component_config_filename(path, translate)
    return webpack(filename, watch_source_files=watch_source_files)

# TODO: replace this with a deterministic config file writer in webpack
COMPONENT_CONFIG_FILES = {}


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


def get_webpack_config(path, translate=None):
    var = get_var_from_path(path)

    # TODO: clean up and scrap resolve?
    # TODO: probably easiest to rely on node_modules babel-loader and provide a `path_to_react` arg
    # TODO: actually, given that this is a pure convenience thing, I think just make it as rigid as possible
    node_modules = os.path.join(service_host_settings.SOURCE_ROOT, 'node_modules')

    translate_config = ''
    if translate:
        # JSX + ES6/7 support
        translate_config += BUNDLE_TRANSLATE_CONFIG.format(
            ext=os.path.splitext(path)[-1],
            node_modules=node_modules
        )

    dev_tool_config = ''
    if settings.DEV_TOOL:
        dev_tool_config = DEV_TOOL_CONFIG

    return BUNDLE_CONFIG.format(
        path_to_react=os.path.join(node_modules, 'react'),
        dir=os.path.dirname(path),
        file='./' + os.path.basename(path),
        var=var,
        translate_config=translate_config,
        dev_tool_config=dev_tool_config,
    )


def get_var_from_path(path):
    var = '{parent_dir}__{filename}'.format(
        parent_dir=os.path.basename(os.path.dirname(path)),
        filename=os.path.splitext(os.path.basename(path))[0]
    )
    return re.sub(r'\W+', '_', var)