import sys
import os
from django.utils import six
from django_node.base_service import BaseService
from django_node.exceptions import NodeServiceError
from ..exceptions import RenderingError
from ..settings import WATCH_COMPONENT_SOURCE


class RenderService(BaseService):
    path_to_source = os.path.join(os.path.dirname(__file__), 'render.js')
    package_dependencies = os.path.dirname(__file__)

    def render(self, path_to_source, to_static_markup, serialized_props=None):
        try:
            response = self.send(
                path_to_source=path_to_source,
                to_static_markup=to_static_markup,
                serialized_props=serialized_props,
                watch_component_source=WATCH_COMPONENT_SOURCE,
            )
        except NodeServiceError as e:
            six.reraise(RenderingError, RenderingError(*e.args), sys.exc_info()[2])

        return response.text