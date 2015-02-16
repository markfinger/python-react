import sys
import os
from django_node import npm
from django_node.exceptions import NodeServerError
from django_node.server import server
from django.utils import six
from .exceptions import RenderingError
from .settings import INVALIDATE_CACHE

RENDER_SERVICE_DIR = os.path.dirname(__file__)
PATH_TO_RENDER_SERVICE_SOURCE = os.path.join(RENDER_SERVICE_DIR, 'renderer.js')

# Ensure that the required packages have been installed
npm.install(RENDER_SERVICE_DIR)

# Start the rendering service
service = server.add_service('/django-react/v1/render', PATH_TO_RENDER_SERVICE_SOURCE)


def render(path_to_source, render_to, path_to_serialized_props=None):
    params = {
        'path-to-source': path_to_source,
        'render-to': render_to,
    }

    if path_to_serialized_props is not None:
        params['path-to-serialized-props'] = path_to_serialized_props

    if INVALIDATE_CACHE:
        params['invalidate-cache'] = 'true'

    try:
        response = service(**params)
    except NodeServerError as e:
        six.reraise(RenderingError, RenderingError(*e.args), sys.exc_info()[2])

    return response.text