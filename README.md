python-react
============

[![Build Status](https://travis-ci.org/markfinger/python-react.svg?branch=master)](https://travis-ci.org/markfinger/python-react)

Python utils for server-side rendering with React.

```python
from react.render import render_component

rendered = render_component(
    '/path/to/component.jsx',
    props={
        'foo': 'bar',
        'woz': [1,2,3],
    }
)

# The rendered markup
print(rendered)
```


Documentation
-------------

- [Installation](#installation)
- [Basic usage](#basic-usage)
- [API](#api)
  - [render_component](#render_component)
  - [RenderedComponent](#renderedcomponent)
- [Django integration](#django-integration)
- [Settings](#settings)
- [Running the tests](#running-the-tests)


Installation
------------

```bash
pip install react
```


Basic usage
-----------

python-react provides a high-level interface to a server which is capable of rendering React components.

To start the server, run

**TODO: once the example's settled**

Render requests should provide a path to a JS file that exports a React component

```python
from react.render import render_component

rendered = render_component('path/to/component.jsx')

print(rendered)
```

The object returned can be passed directly into your template layer.



API
---


### render_component

Renders a component to its initial HTML. You can use this method to generate HTML on the server 
and send the markup down on the initial request for faster page loads and to allow search engines 
to crawl your pages for SEO purposes.

Returns a [RenderedComponent](#renderedcomponent) instance which can be passed directly into your 
front end to output the component's markup and to mount the component for client-side interactivity.


#### Usage

```python
from react.render import render_component

render_component(
    # A absolute path to a file which exports your React component
    path='...',

    # An optional dictionary of data that will be passed to the renderer
    # and can be reused on the client-side
    props = {
        'foo': 'bar'
    },

    # An optional boolean indicating that React's `renderToStaticMarkup` method
    # should be used, rather than `renderToString`
    to_static_markup = False,

    # An optional class which is used to encode the props to JSON
    json_encoder=None,
)
```

If you are using python-react in a Django project, relative paths to components will be resolved
via Django's static file finders.


### RenderedComponent

An object representing the output from the rendering process

```
rendered = render_component(
    'path/to/component.jsx',
    props={
        # ...
    },
)

# The markup generated from rendering the component with the provided props
rendered.markup

# The value of the `props` argument serialized to JSON. You can pass this directly
# into your template layer
rendered.props

# Equivalent to `rendered.markup`
str(rendered)
unicode(rendered)
```


Settings
--------

Settings can be defined by calling `react.conf.settings.configure` with keyword arguments matching 
the setting that you want to define. For example

```python
from react.conf import settings

settings.configure(
    RENDER_URL='http://127.0.0.1:8001/render',
)
```

If you are using python-react in a Django project, add `'react'` to your `INSTALLED_APPS`

```python
INSTALLED_APPS = (
    # ...
    'react',
)
```

To configure python-react, place a dictionary named `REACT` into your settings file. For example

REACT = {
    'RENDER_URL': 'http://127.0.0.1:8001/render'
}


### RENDER_URL

A complete url to an endpoint which accepts POST requests conforming to react-render's configuration API.

Default: `'http://127.0.0.1:9009`


Running the tests
-----------------

```bash
pip install -r requirements.txt
npm install
python runtests.py
```
