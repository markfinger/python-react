import os
import tempfile
from django.utils import six
from django_node import npm
from django_node.utils import dynamic_import
from .settings import NPM_INSTALL_ON_INIT, RENDERER
from .settings import
from .exceptions import SourceFileNotFound

# Allow the renderer to be defined in settings
renderer = dynamic_import(RENDERER)

if NPM_INSTALL_ON_INIT:
    # Ensure that the required packages have been installed
    npm.install(os.path.dirname(__file__))


def render_component(path_to_source, serialized_props=None, to_static_markup=None):
    if not path_to_source or not os.path.exists(path_to_source):
        raise SourceFileNotFound(path_to_source)

    if to_static_markup is None:
        render_to = 'string'
    else:
        render_to = 'static'

    if serialized_props:
        with tempfile.NamedTemporaryFile() as serialized_props_file:
            serialized_props_file.write(six.b(serialized_props))
            serialized_props_file.flush()
            path_to_serialized_props = serialized_props_file.name

            return renderer(path_to_source, render_to, path_to_serialized_props)

    return renderer.render(path_to_source, render_to)