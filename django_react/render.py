import os
from django.contrib.staticfiles import finders
from django_node import npm
from .settings import NPM_INSTALL_ON_INIT
from .exceptions import SourceFileNotFound
from .services import RenderService


if NPM_INSTALL_ON_INIT:
    # Ensure that the required packages have been installed
    npm.install(os.path.dirname(__file__))

render_service = RenderService()


def render_component(path_to_source, serialized_props=None, to_static_markup=None):
    if os.path.isabs(path_to_source):
        if not os.path.exists(path_to_source):
            raise SourceFileNotFound(path_to_source)
    else:
        absolute_path_to_source = finders.find(path_to_source)
        if absolute_path_to_source:
            path_to_source = absolute_path_to_source
        else:
            raise SourceFileNotFound(path_to_source)

    if to_static_markup is None:
        render_to = 'STRING'
    else:
        render_to = 'STATIC'

    return render_service.render(path_to_source, render_to, serialized_props)