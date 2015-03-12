import sys
import os
from django.utils import six
from django_node.base_service import BaseService
from django_node.exceptions import NodeServiceError
from ..exceptions import ComponentRenderingError


class RenderService(BaseService):
    path_to_source = os.path.join(os.path.dirname(__file__), 'render.js')
    package_dependencies = os.path.dirname(__file__)

    def render(self, path_to_source, serialized_props, to_static_markup, watch_source):
        try:
            response = self.send(
                path_to_source=path_to_source,
                serialized_props=serialized_props,
                to_static_markup=to_static_markup,
                watch_source=watch_source,
            )
        except NodeServiceError as e:
            six.reraise(ComponentRenderingError, ComponentRenderingError(*e.args), sys.exc_info()[2])

        return response.text