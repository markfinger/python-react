import os
import tempfile
import importlib
from django_node import npm, node
from .settings import NPM_VERSION_REQUIRED, NODE_VERSION_REQUIRED, RENDERER
from .exceptions import SourceFileNotFound, RendererImportError


# Ensure that the external dependencies are met
node.ensure_version_gte(NODE_VERSION_REQUIRED)
npm.ensure_version_gte(NPM_VERSION_REQUIRED)

# Ensure that the required packages have been installed
npm.install(os.path.dirname(__file__))

# Import the renderer defined in django_react.settings
renderer_module_import_path = '.'.join(RENDERER.split('.')[:-1])
try:
    renderer_module = importlib.import_module(renderer_module_import_path)
    renderer_class = getattr(renderer_module, RENDERER.split('.')[-1])
except (ImportError, AttributeError):
    raise RendererImportError('Failed to import django-react renderer "{renderer}"'.format(
        renderer=RENDERER
    ))
renderer = renderer_class()


def render_component(path_to_source, serialized_props=None, to_static_markup=None):
    if not path_to_source or not os.path.exists(path_to_source):
        raise SourceFileNotFound(path_to_source)

    if to_static_markup is None:
        render_to = 'string'
    else:
        render_to = 'static'

    if serialized_props:
        with tempfile.NamedTemporaryFile() as serialized_props_file:
            serialized_props_file.write(serialized_props)
            serialized_props_file.flush()
            path_to_serialized_props = serialized_props_file.name

            return renderer.render(path_to_source, render_to, path_to_serialized_props)

    return renderer.render(path_to_source, render_to)