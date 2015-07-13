python-react
============

[![Build Status](https://travis-ci.org/markfinger/python-react.svg?branch=master)](https://travis-ci.org/markfinger/python-react)

Server-side rendering of React components with data from your Python system

```python
from react.render import render_component

rendered = render_component(
    '/path/to/component.jsx',
    {
        'foo': 'bar',
        'woz': [1,2,3],
    }
)

print(rendered)
```

For client-side side integrations, refer to the [docs](#using-react-on-the-front-end).


Documentation
-------------

- [Installation](#installation)
- [Basic usage](#basic-usage)
  - [Setting up a render server](#setting-up-a-render-server)
- [Using React on the front-end](#using-react-on-the-front-end)
- [render_component](#render_component)
- [Render server](#render-server)
  - [Usage in development](#usage-in-development)
  - [Usage in production](#usage-in-production)
  - [Overriding the renderer](#overriding-the-renderer)
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

python-react provides an interface to a render server which is capable of rendering React components with data
from your python process.

Render requests should provide a path to a JS file that exports a React component. If you want to pass
data to the component, you can optionally provide a second argument that will be used as the component's 
`props` property.

```python
from react.render import render_component

rendered = render_component('path/to/component.jsx', {'foo': 'bar'})

print(rendered)
```

The object returned has two properties:

 - `markup` - the rendered markup
 - `props` - the JSON-serialized props

If the object is coerced to a string, it will emit the value of the `markup` attribute.


### Setting up a render server

Render servers are typically Node.js processes which sit alongside the python process and respond to network requests.

To add a render server to your project, you can refer to the [basic rendering example](examples/basic_rendering) 
for a simple server that will cover most cases. The key files for the render server are: 
 - [server.js](examples/basic_rendering/server.js) - the server's source code
 - [package.json](examples/basic_rendering/package.json) - the server's dependencies, installable with 
   [npm](http://npmjs.com)


Using React on the front-end
----------------------------

There are a number of way in which you can integrate React into the frontend of a Python system. Generally,
you will want to a JS build tool and a python package which can read in it's output.

The two most popular build tools are:

- [Webpack](https://webpack.github.io) is currently the recommended build tool for frontend projects. It can
  compile your files into browser-executable code and provides a variety of tools and processes which can 
  simplify complicated workflows.
- [Browserify](http://browserify.org/) is another popular tool and has a lot of cross-over with webpack. It
  is argurably the easiest of the two to use, but it tends to lag behind webpack in certain functionalities.

For React projects, you'll find that webpack is the usual recommendation. Webpack's hot module replacement, 
code-splitting, and a wealth of loaders are the features typically cited. 
[react-hot-loader](https://github.com/gaearon/react-hot-loader) is a particularly useful tool as it allows
changes to your components to be streamed live into your browser.

To integrate webpack's output into a python system, the two most popular solutions are:

- [django-webpack-loader](https://github.com/owais/django-webpack-loader) - uses a webpack plugin to generates
  a file for your python process to consume. Tends to be simpler to reason about, does one thing and does it 
  well. Requires you to interact with webpack directly.
- [python-webpack](https://github.com/markfinger/python-webpack) - talks to a build server that wraps around
  webpack. Tends to be more complex, but offers more features. Requires you to run a build server.

For most use-cases, both tools will provide similar functionalities. django-webpack-loader puts you in direct
control of webpack's processes, so it's a good starting point to learn about the tool. python-webpack
abstracts away webpack, so it may be easier to integrate.

Note: older versions of this library used to provide tools for integrating React into your frontend. While 
they provided some conveniences they also overly complicated deployments, limited the functionalities that 
you could apply, and locked you in to a workflow which was contrary to React's best practices. If you want to
persist with the worflow previously offered, the [self-mounting components example](examples) illustrates the
wiring necessary to achieve comparable functionality.


render_component
----------------

Renders a component to its initial HTML. You can use this method to generate HTML on the server 
and send the markup down on the initial request for faster page loads and to allow search engines 
to crawl your pages for SEO purposes.


#### Usage

```python
from react.render import render_component

render_component(
    # A path to a file which exports your React component
    path='...',

    # An optional dictionary of data that will be passed to the renderer
    # and can be reused on the client-side.
    props={
        'foo': 'bar'
    },

    # An optional boolean indicating that React's `renderToStaticMarkup` method
    # should be used, rather than `renderToString`
    to_static_markup=False,

    # An optional object which will be used instead of the default renderer
    renderer=None,
)
```

If you are using python-react in a Django project, relative paths to components will be resolved
via Django's static file finders.

By default, render_component relies on access to a render server that exposes an endpoint compatible
with [react-render's API](https://github.com/markfinger/react-render). If you want to use a different
renderer, pass in an object as the `renderer` arg. The object should expose a `render` method which
accepts the `path`, `data`, and `to_static_markup` arguments.


Render server
-------------

Earlier versions of this library would run the render server as a subprocess, this tended to make development
easier, but introduced instabilities and opaque behaviour. To avoid these issues python-react now relies on 
externally managed process. While managing extra processes can add more overhead initially, it avoids pain down
the track.

If you only want to run the render server in particular environments, change the `RENDER` setting to
False. When `RENDER` is False, the render server is not used directly, but it's wrapper will return similar 
objects with the `markup` attribute as an empty string.


### Usage in development

In development environments, it can be easiest to set the `RENDER` setting to False. This ensures that the 
render server will not be used, hence you only need to manage your python process.

Be aware that the render servers provided in the example and elsewhere rely on Node.js's module system
which - similarly to Python - caches all modules as soon as they are imported. If you use the render
server in a development environment, your code is cached and your changes will **not** effect the
rendered markup until you reset the render server.


### Usage in production

In production environments, you should ensure that `RENDER` is set to True.

You will want to run the render server under whatever supervisor process suits your need. Depending on
your setup, you may need to change the `RENDER_URL` setting to reflect your setup.

When the render server wrapper connects to the JS process, it adds a `?hash=<SHA1>` parameter to the url. The
hash parameter is generated from the serialized data that is sent in the request's body and is intended
for consumption by caching layers.

Depending on your load, you may want to put a reverse proxy in front of the render server. Be aware that
render server requests are sent as POST requests and many reverse proxies are configured by default to 
**not** cache POST requests.


### Overriding the renderer

If you want to override the default renderer, one approach is to create a wrapper function so that
you can consistently define the `renderer` argument to `render_component`. For example:

```python
from react.render import render_component

class MyRenderer(object):
    def render(self, path, props=None, to_static_markup=False):
        # ...

def my_render_function(*args, **kwargs):
    kwargs['renderer'] = MyRenderer()
    return render_component(*args, **kwargs)
```


Settings
--------

If you are using python-react in a non-django project, settings can be defined by calling
`react.conf.settings.configure` with keyword arguments matching the setting that you want to define.
For example:

```python
from react.conf import settings

DEBUG = True

settings.configure(
	RENDER=not DEBUG,
    RENDER_URL='http://127.0.0.1:9009/render',
)
```

If you are using python-react in a Django project, add `'react'` to your `INSTALLED_APPS` and define
settings in a `REACT` dictionary.

```python
INSTALLED_APPS = (
    # ...
    'react',
)

REACT = {
	'RENDER': not DEBUG,
    'RENDER_URL': 'http://127.0.0.1:8001/render',
}
```


### RENDER

A flag denoting that the render server should be used. If set to `False`, the renderer will return
objects with an empty string as the `markup` attribute.

Pre-rendering your components is only intended for environments where serving markup quickly is a must.
In a live development environment, running multiple processes overly complicates your setup and can lead
to inexplicable behaviour due to the render server's file caches. Setting this to `False` will remove the
need to run a render server next to your python server.

Default: `True`


### RENDER_URL

A complete url to an endpoint which accepts POST requests conforming to
[react-render's API](https://github.com/markfinger/react-render).

Default: `'http://127.0.0.1:9009/render'`


Running the tests
-----------------

```bash
pip install -r requirements.txt
npm install
python runtests.py
```
