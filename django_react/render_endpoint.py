import os
from django_node.server_endpoint import ServerEndpoint
from django_node.exceptions import NodeServerError
from .exceptions import RenderingError


class ReactRenderEndpoint(ServerEndpoint):
    root_url = '/django-react'

    def render(self, path_to_source, render_to, path_to_serialized_props=None):
        params = {
            'path-to-source': path_to_source,
            'render-to': render_to,
        }

        if path_to_serialized_props is not None:
            params['path-to-serialized-props'] = path_to_serialized_props

        try:
            response = self.get(params=params)
        except NodeServerError as e:
            raise RenderingError(*e.args)

        return response.text

__endpoint_singleton = ReactRenderEndpoint(
    url='/render',
    path_to_source=os.path.join(os.path.dirname(__file__), 'render-endpoint.js')
)


def get_endpoint():
    return __endpoint_singleton