import os
from django.shortcuts import render
from django_node.utils import resolve_dependencies
from django_react import ReactComponent

resolve_dependencies(path_to_run_npm_install_in=os.path.dirname(__file__))


def index(request):
    component = ReactComponent(
        'example_app/HelloWorld.jsx',
        name='World'
    )
    return render(request, 'example_app/index.html', {
        'component': component,
    })