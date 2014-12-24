import os
import tempfile
from django_node import npm, node
import settings
import exceptions


# Ensure that the external dependencies are met
node.ensure_version_gte(settings.NODE_VERSION_REQUIRED)
npm.ensure_version_gte(settings.NPM_VERSION_REQUIRED)

# Ensure that the required packages have been installed
npm.install(os.path.dirname(__file__))


def render(path_to_source, serialized_props=None, to_static_markup=None):
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
            settings.PATH_TO_RENDERER,
            '--path-to-source', path_to_source,
            '--render-to', render_to,
            '--serialized-props', serialized_props_file.name,
        )

        # While rendering templates Django will silently ignore some types of exceptions,
        # so we need to intercept them and raise our own class of exception
        try:
            stderr, stdout = node.run(*arguments, production=settings.DEBUG)
        except (TypeError, AttributeError) as e:
            raise exceptions.RenderingError(e.__class__.__name__, *e.args)

        if stderr:
            raise exceptions.RenderingError(stderr)

        return stdout