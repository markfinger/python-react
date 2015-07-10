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


Documentation
-------------

- [Installation](#installation)
- [Basic usage](#basic-usage)
  - [Setting up a render server](#setting-up-a-render-server)
- [render_component](#render_component)
- [Render server](#render-server)
  - [Usage in development](#usage-in-development)
  - [Usage in production](#usage-in-production)
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

python-react provides an interface to a render server which is capable of rendering React components.

Render requests should provide a path to a JS file that exports a React component

```python
from react.render import render_component

rendered = render_component('path/to/component.jsx')

print(rendered)
```

The object returned has two properties:

 - `markup` - the rendered markup
 - `props` - the JSON serialized props (if any were provided)

The object can be coerced to a string to output the markup. Hence you can dump the object directly into
your template layer.


### Setting up a render server

Render servers are typically Node.js processes which sit alongside the python process and respond to network requests. 

To add a render server to your project, you can refer to the [basic rendering example](examples/basic_rendering) 
for a basic server which will cover most cases. The key files for the render server are the `server.js` and `package.json` files.


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
    data={
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

Earlier versions of this library used to run the render server as a subprocess, this tended to make
development easier, but tended to introduce instabilities and inexplicable behaviour. The library
now relies on externally managed process.

If you only want to run the render server in particular environments, change the `RENDER` setting to
False. When `RENDER` is False, the render server is not used, but the similar objects are returned.
This enables you to easily build a codebase that supports both development and production environments.


### Usage in development

In development environments, it's often easiest to set `RENDER` to False. This ensures that the render
server will not be used, hence you only need to manage your python process.

Be aware that the render servers provided in the example and elsewhere rely on Node.js's module system
which - similarly to Python - caches all modules as soon as they are imported. If you use the render
server in a development environment, your code is cached and your changes will **not** effect the
rendered markup until you reset the render server.


### Usage in production

In production environments, you should ensure that `RENDER` is set to True.

You will want to run the render server under whatever supervisor process suits your need. Depending on
your setup, you may need to change the `RENDER_URL` setting to reflect your setup.

Requests are sent to the render server as POST requests.

The render server connector that ships with python-react adds a `?hash=<SHA1>` parameter to the url. The
hash parameter is generated from the serialized data that is sent in the request's body and is intended
for consumption by caching layers.

Depending on your load, you may want to put a reverse proxy in front of the render server. Be aware that
many reverse proxies are configured by default to **not** cache POST requests.


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
