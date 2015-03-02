import sys
import os
from django.utils import six
from django_node.base_service import BaseService
from django_node.exceptions import NodeServiceError
from django_node.utils import resolve_dependencies
from .exceptions import RenderingError
from .settings import WATCH_COMPONENT_SOURCE


# Ensure that the required packages have been installed
resolve_dependencies(
    path_to_run_npm_install_in=os.path.dirname(__file__)
)


class RenderService(BaseService):
    path_to_source = os.path.join(os.path.dirname(__file__), 'services', 'render.js')

    def render(self, path_to_source, render_to, serialized_props=None):
        try:
            response = self.send(
                path_to_source=path_to_source,
                render_to=render_to,
                serialized_props=serialized_props,
                watch_component_source=WATCH_COMPONENT_SOURCE,
            )
        except NodeServiceError as e:
            six.reraise(RenderingError, RenderingError(*e.args), sys.exc_info()[2])

        return response.text