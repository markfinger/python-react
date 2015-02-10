import sys
import os
from django_node import npm
from django_node.exceptions import NodeServerError
from django_node.server import server
from django.utils import six
from .exceptions import RenderingError

# Ensure that the required packages have been installed
npm.install(os.path.dirname(__file__))

render_endpoint = server.add_endpoint(
    endpoint='/django-react/render',
    path_to_source=os.path.join(os.path.dirname(__file__), 'renderer.js')
)


def render(path_to_source, render_to, path_to_serialized_props=None):
    params = {
        'path-to-source': path_to_source,
        'render-to': render_to,
    }

    if path_to_serialized_props is not None:
        params['path-to-serialized-props'] = path_to_serialized_props

    try:
        response = render_endpoint.get(params=params)
    except NodeServerError as e:
        six.reraise(RenderingError, RenderingError(*e.args), sys.exc_info()[2])

    return response.text