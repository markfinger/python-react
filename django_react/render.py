import os
import tempfile
from django_node import npm, node
from .settings import PATH_TO_RENDERER, NPM_VERSION_REQUIRED, NODE_VERSION_REQUIRED, DEBUG
from .exceptions import RenderingError, SourceFileNotFound


# Ensure that the external dependencies are met
node.ensure_version_gte(NODE_VERSION_REQUIRED)
npm.ensure_version_gte(NPM_VERSION_REQUIRED)

# Ensure that the required packages have been installed
npm.install(os.path.dirname(__file__))


def render_component(path_to_source, serialized_props=None, to_static_markup=None):
    if not path_to_source or not os.path.exists(path_to_source):
        raise SourceFileNotFound(path_to_source)

    if serialized_props is None:
        serialized_props = '{}'

    if to_static_markup is None:
        render_to = 'string'
    else:
        render_to = 'static'

    with tempfile.NamedTemporaryFile() as serialized_props_file:
        serialized_props_file.write(serialized_props)
        serialized_props_file.flush()

        arguments = (
            PATH_TO_RENDERER,
            '--path-to-source', path_to_source,
            '--render-to', render_to,
            '--serialized-props-file', serialized_props_file.name,
        )

        # While rendering templates Django will silently ignore some types of exceptions,
        # so we need to intercept them and raise our own class of exception
        try:
            stderr, stdout = node.run(*arguments, production=DEBUG)
        except (TypeError, AttributeError) as e:
            raise RenderingError(e.__class__.__name__, *e.args)

        if stderr:
            raise RenderingError(stderr)

        # `console.log` appends a new line to the render output
        if stdout.endswith('\n'):
            stdout = stdout[:-1]

        return stdout