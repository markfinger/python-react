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


def _render(path_to_source, serialised_props, to_static_markup=None):
    with tempfile.NamedTemporaryFile() as serialised_props_file:
        serialised_props_file.write(serialised_props)
        serialised_props_file.flush()

        arguments = (
            settings.PATH_TO_RENDERER,
            '--path-to-source', path_to_source,
            '--render-to', 'static' if to_static_markup else 'string',
            '--serialised-props', serialised_props_file.name,
        )

        # Django will silently ignore some types of exceptions, so we need to
        # intercept them and raise our own class of exception
        try:
            stderr, stdout = node.run(*arguments)
        except (TypeError, AttributeError) as e:
            raise exceptions.RenderingError(e.__class__.__name__, *e.args)

        if stderr:
            raise exceptions.RenderingError(stderr)

        return stdout


def render_to_string(path_to_source, serialised_props):
    return _render(path_to_source, serialised_props)


def render_to_static_markup(path_to_source, serialised_props):
    return _render(path_to_source, serialised_props, to_static_markup=True)