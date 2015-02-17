import os
from django.shortcuts import render
from django_node import npm
from django_react import ReactComponent

# Ensure that the JS dependencies are installed
npm.install(os.path.dirname(__file__))


class MyComponent(ReactComponent):
    source = 'example/HelloWorld.jsx'


def index(request):
    component = MyComponent(name='World')
    return render(request, 'example/index.html', {
        'component': component,
    })