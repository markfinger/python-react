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

For client-side integrations, refer to the [docs](#using-react-on-the-front-end).


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
- [Settings](#settings)
- [Frequently Asked Questions](#frequently-asked-questions)
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
 - `data` - the data returned by the render server

If the object is coerced to a string, it will emit the value of the `markup` attribute.


### Setting up a render server

Render servers are typically Node.js processes which sit alongside the python process and respond to network requests.

To add a render server to your project, you can refer to the [basic rendering example](examples/basic_rendering)
for a simple server that will cover most cases. The key files for the render server are:
 - [render_server.js](examples/basic_rendering/render_server.js) - the server's source code
 - [package.json](examples/basic_rendering/package.json) - the server's dependencies, installable with
   [npm](http://npmjs.com)


Using React on the front-end
----------------------------

There are a number of ways in which you can integrate React into the frontend of a Python system. The typical
setup involves a build tool and a python package that can integrate it.

The two most popular build tools are:

- [Webpack](https://webpack.github.io) - compiles your files into browser-executable code and provides a
  variety of tools and processes which can simplify complicated workflows.
- [Browserify](http://browserify.org/) - has a lot of cross-over with webpack. Is argurably the easiest of the
  two to use, but it tends to lag behind webpack in functionality.

For React projects, you'll find that webpack is the usual recommendation. Webpack's hot module replacement,
code-splitting, and a wealth of loaders are the features typically cited as being irreplaceable.
[react-hot-loader](https://github.com/gaearon/react-hot-loader) is a particularly useful tool, as it allows
changes to your components to be streamed live into your browser.

If you want to integrate webpack's output into your python system, you can either hard-code the paths or you
can use a manifest plugin that provides a way for your python system to introspect the compiler's state.

The most popular manifest tool is [owais/django-webpack-loader](https://github.com/owais/django-webpack-loader).
Owais has provided a great set of docs and examples, so it's your best bet for integrating webpack into your
project.

If you aren't running a Django system, or you need portable manifests that can be decoupled and deployed,
[markfinger/python-webpack-manifest](https://github.com/markfinger/python-webpack-manifest) might suit your
needs.

There's also [markfinger/python-webpack](https://github.com/markfinger/python-webpack), but it's a bit more
heavy handed, abstract, and is only of use if you need a really tight coupling between your python and
javascript worlds.


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

    # An optional dictionary of request header information (such as `Accept-Language`)
    # to pass along with the request to the render server
    request_headers={
        'Accept-Language': 'da, en-gb;q=0.8, en;q=0.7'
    },

    # An optional timeout that is used when handling communications with the render server.
    # Can be an integer, a float, or a tuple containing two numeric values (the two values
    # represent the individual timeouts on the send & receive phases of the request).
    # Note that if not defined, this value will default to (5, 5)
    timeout=None
)
```

If you are using python-react in a Django project, relative paths to components will be resolved
via Django's static file finders.

By default, render_component relies on access to a render server that exposes an endpoint compatible
with [react-render's API](https://github.com/markfinger/react-render). If you want to use a different
renderer, pass in an object as the `renderer` arg. The object should expose a `render` method which
accepts the `path`, `data`, `to_static_markup`, and `request_headers` arguments.


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

Be aware that the render servers provided in the examples and elsewhere rely on Node.js's module system
which - similarly to Python - caches all modules as soon as they are imported. If you use the render
server in a development environment, your code is cached and your changes will **not** effect the
rendered markup until you reset the render server.


### Usage in production

In production environments, you should ensure that `RENDER` is set to True.

You will want to run the render server under whatever supervisor process suits your need. Depending on
your setup, you may need to change the `RENDER_URL` setting to reflect your environment.

The render server should be run with the `NODE_ENV` environment variable set to `production`, 
eg: `NODE_ENV=production node render_server.js`. React defaults to development mode and relies on the 
`NODE_ENV` variable to deactivate dev-oriented code (types and constraint checking) that slows down renders. 
Defining this variable will ensure that your code is rendered much faster.

Depending on your load, you may want to use a worker farm to handle rendering. Node's
[cluster module](https://nodejs.org/api/cluster.html) provides an easy way to fork a process and serve
multiple instances from a single network address.

An alternative to worker farms is to put a cache in front of the render server. Be aware that
render server requests are sent as POST requests and most reverse proxies have issues with 
caching POST requests.

When the render server wrapper connects to the JS process, it adds a `?hash=...` parameter to the url. The
hash parameter is a SHA-1 hash of the serialized data that is sent in the request's body and is intended
for consumption by caching layers.

Another alternative is to wire the calls to the render server into your caching system. If you override the
`renderer` kwarg, you could wrap the call to the server to first check if the data is available locally and
fallback to populating the cache with the rendered markup.


### Overriding the renderer

If you want to override the default renderer, one approach is to create a wrapper function so that
you can consistently define the `renderer` argument to `render_component`. For example:

```python
from react.render import render_component

class MyRenderer(object):
    def render(self, path, props=None, to_static_markup=False, request_headers=None, timeout=None):
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


Frequently Asked Questions
--------------------------

### How do I return extra data from the render server?

You can edit the render server's code and annotate the returned payload with whatever data 
that you like. The payload provided by the render server is available under the `data` attribute 
of the response object.

For example:

```python
from react.render import render_component

rendered = render_component('path/to/component.js')

print(rendered.data)
```

### Can python-react integrate with Django?

python-react can integrate with Django's settings and the renderer integration can 
resolve relative paths to components via django's static file finders.

### How do I handle Django's translation and gettext with React components?

[sillygod](https://github.com/sillygod) sparked a discussion of this at issue 
[#69](https://github.com/markfinger/python-react/issues/69).

### Can python-react integrate with Web2Py?

[Anima-t3d](https://github.com/Anima-t3d) has a write-up of their experience
in [#70](https://github.com/markfinger/python-react/issues/70#issuecomment-254396083).

### How do I pass child components to the root component?

[Anima-t3d](https://github.com/Anima-t3d) sparked a discussion of this at issue 
[#71](https://github.com/markfinger/python-react/issues/71).


Running the tests
-----------------

```bash
pip install -r requirements.txt
npm install
python runtests.py
```
