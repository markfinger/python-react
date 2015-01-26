from django_node import node
from .settings import PATH_TO_RENDERER_SOURCE, DEBUG
from .exceptions import RenderingError


class ReactRenderer(object):
    """
    Temporarily spins up a new Node instance to render the component.

    django_react.server.ReactRenderServer is recommended for general use,
    as it is overwhelmingly faster than this renderer.

    The primary use-case for ReactRenderer is situations in which you may
    wish to avoid a persistent process on your network or a persistent
    JavaScript environment rendering your components.
    """

    @staticmethod
    def render(path_to_source, render_to, path_to_serialized_props=None):
        arguments = (
            PATH_TO_RENDERER_SOURCE,
            '--path-to-source', path_to_source,
            '--render-to', render_to,
        )

        if path_to_serialized_props is not None:
            arguments += (
                '--path-to-serialized-props', path_to_serialized_props
            )

        # While rendering templates Django will silently ignore some types of exceptions,
        # so we need to intercept them and raise our own class of exception
        try:
            stderr, stdout = node.run(*arguments, production=DEBUG)
        except (TypeError, AttributeError) as e:
            raise RenderingError(e.__class__.__name__, *e.args)

        if stderr:
            raise RenderingError(stderr)

        return stdout