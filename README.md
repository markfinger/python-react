python-react
============

[![Build Status](https://travis-ci.org/markfinger/python-react.svg?branch=master)](https://travis-ci.org/markfinger/python-react)

Server-side rendering, client-side mounting, JSX translation, and component bundling.

```python
from react.render import render_component

component = render_component(
    # A path to a file exporting your React component
    '/path/to/component.jsx',
    # Translate the source to JavaScript from JSX + ES6/7
    translate=True,
    # Props that will be passed to the renderer and reused on 
    # the client-side to provide immediate interactivity
    props={
        'foo': 'bar',
        'woz': [1,2,3],
    }
)

# The rendered markup
print(component)

# Outputs JavaScript which will mount the component on the client-side and
# provide immediate interactivity
print(component.render_js())
```

If you only want to plug your JSX files into the client-side, you can translate the source code and
bundle it into a single file by using `bundle_component`.

```python
from react.bundle import bundle_component

bundle = bundle_component(
    # A path to a file exporting your React component
    '/path/to/component.jsx',
    # Translate the source to JavaScript from JSX + ES6/7
    translate=True
)

# Renders a script element pointing to the bundled component
print(bundle.render())

# Outputs the global variable name that the component is exposed as.
print(bundle.get_var())
```


Documentation
-------------

- [Installation](#installation)
- [API](#api)
  - [render_component()](#render_component)
  - [RenderedComponent](#renderedcomponent)
  - [bundle_component()](#bundle_component)
- [Django integration](#django-integration)
- [Settings](#settings)
- [Running the tests](#running-the-tests)


Installation
------------

python-react depends on [js-host](https://github.com/markfinger/python-js-host/) to provide
interoperability with JavaScript. Complete its 
[quick start](https://github.com/markfinger/python-js-host/#quick-start) before continuing.

Install [python-webpack](https://github.com/markfinger/python-webpack)

Install python-react's JS dependencies

```bash
npm install --save react react-render
```

Add react-render to the functions definition of your `host.config.js` file

```javascript
var reactRender = require('react-render');

module.exports = {
  functions: {
    // ...
    react: reactRender
  }
};
```

And install python-react

```bash
pip install react
```


API
---


### render_component()

Renders a component to its initial HTML. You can use this method to generate HTML on the server 
and send the markup down on the initial request for faster page loads and to allow search engines 
to crawl your pages for SEO purposes.

Returns a [RenderedComponent](#renderedcomponent) instance which can be passed directly into your 
front end to output the component's markup and to mount the component for client-side interactivity.


#### Usage

```python
from react.render import render_component

render_component(
    # A path to a file which exports your React component
    path='...',
    # An optional dictionary of data that will be passed to the renderer
    # and can be reused on the client-side
    props = {
        'foo': 'bar'
    },
    # An optional boolean indicating that the component should be bundled and 
    # translated from JSX and ES6/7 before rendering. Components are translated 
    # with Babel
    translate = True,
    # An optional boolean indicating that the component should be bundled for
    # before rendering. If `translate` is set to True, this argument is ignored
    bundle = True,
    # An optional boolean indicating that React's `renderToStaticMarkup` method 
    # should be used, rather than `renderToString`
    to_static_markup = False,
    # An optional class which is used to encode the props to JSON
    json_encoder=None,
)
```


### RenderedComponent

The result of rendering a component to its initial markup. RenderedComponents can be converted to 
strings to output their generated markup. If `translate` or `bundle` was provided to `render_component`, 
they can also be mounted on the client-side to provide immediate interactivity.

```python
component = render_component(...)

# Outputs the generated markup
str(component)

# Also outputs the generated markup
component.render_markup()

# Render JS which will mount the component over the rendered markup.
# This enables you to provide immediate interactivity
component.render_js()
```

Note: if you wish to use the `render_js` method on the client-side, you **must** provide a 
`<script>` element pointing to React. React is omitted from the bundled component so that 
build times are reduced, and to ensure that multiple components can be included on a single 
page without duplicating React's codebase.

Be aware that the mounting strategy used by `render_js` is only intended for convenience. If you 
want to use a more custom solution for mounting or bundling, there are a couple of helpers provided 
to assist you:

```python
# The data used to render the component, this can be plugged straight into the client-side
component.render_props()

# The bundled component (a WebpackBundle instance)
component.bundle

# Render a script element pointing to the bundled component
print(component.bundle.render())

# The global variable that the bundle will exposes the component as
print(component.get_var())

# When rendering a bundled component, the component is wrapped in a container
# element to allow the mounting JS to target it. You can use this selector to
# target the container element yourself
print(component.get_container_id())

# The rendered markup without the container element wrapping it
print(component.markup)

# Render the JS used to mount the bundled component over the rendered component
print(component.render_mount_js())
```


### bundle_component()

Packages a React component so that it can be re-used on the client-side. JSX + ES6+7 files are translated
to JavaScript with [Babel](https://babeljs.io/).

Be aware that `bundle_component` is primarily a convenience method. Under the hood, it plugs a pre-built 
webpack config file into [python-webpack](https://github.com/markfinger/python-webpack).

If you require more flexibility in the bundling process, you are recommended to read the code to understand
what is happening, and then use python-webpack yourself.


#### Usage

```python
from react.bundle import bundle_component

bundle_component(
    # A path to a file which exports the component. If the path is relative,
    # django's static file finders will attempt to find the file
    path='...',
    # An optional boolean indicating that the component should be translated
    # from JSX and ES6/7 during the bundling process
    translate = True,
)
```


Django integration
------------------

If you are using python-react in a Django project, add `'react'` to your `INSTALLED_APPS`

```python
INSTALLED_APPS = (
    # ...
    'react',
)
```

To configure python-react, place a dictionary named `REACT` into your settings file. For example

```python
REACT = {
    'DEVTOOL': 'eval' if DEBUG else None,
}
```

When calling `render_component` or `bundle_component`, python-react will attempt to use Django's
static file finders to resolve relative paths. If you provide a path such as `'my_app/component.jsx'`,
Django would resolve that path to an app's static folder, eg: `'my_app/static/my_app/component.jsx'`.


Settings
--------

Settings can be defined by calling `react.conf.settings.configure` with keyword arguments matching 
the setting that you want to define. For example

```python
from react.conf import settings

DEBUG = True

settings.configure(
    DEVTOOL='eval' if DEBUG else None,
)
```

### DEVTOOL

The [devtool](http://webpack.github.io/docs/configuration.html#devtool) that webpack uses when 
bundling components.

During development, you are recommended to set this to `'eval'`, as it will assist with debugging
translated and bundled assets.

Default: `None`

### PATH_TO_REACT

An import path that will be used when rendering bundled components.

If not defined, the bundler will default to using js-host's SOURCE_ROOT via `os.path.join(SOURCE_ROOT, 'node_modules', 'react')`.

Default: `None`

### TRANSLATE_TEST

When bundling a component with `translate=True`, this JavaScript regex is tested against every file to 
determine if the babel loader should run over it.

If not defined, the bundler will default to using `'/.jsx$/'`.

Default: `None`


Running the tests
-----------------

```bash
mkvirtualenv django-react
pip install -r requirements.txt
python runtests.py
```
