import os
import hashlib
from django.contrib.staticfiles import finders
from django_node import npm
from .settings import CACHE_RENDERED_HTML, NPM_INSTALL_ON_INIT
from .exceptions import SourceFileNotFound
from .services import RenderService


if NPM_INSTALL_ON_INIT:
    # Ensure that the required packages have been installed
    npm.install(os.path.dirname(__file__))

render_service = RenderService()

RENDER_CACHE = {}

# TODO: cache based on path_to_source + to_static_markup + md5(serialized_props)


def get_cache_key(path_to_source, render_to, serialized_props=None):
    md5 = hashlib.md5()
    if serialized_props is None:
        md5.update('')
    else:
        md5.update(serialized_props)
    return 'django_react-{path_to_source}-{render_to}-{props_hash}'.format(
        path_to_source=path_to_source,
        render_to=render_to,
        props_hash=md5.hexdigest()
    )


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

    if to_static_markup:
        render_to = 'STATIC'
    else:
        render_to = 'STRING'

    # TODO: cache
    cache_key = get_cache_key(path_to_source, render_to, serialized_props)

    return render_service.render(path_to_source, render_to, serialized_props)