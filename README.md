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

# Render JavaScript which will mount the component on the client-side and
# provide immediate interactivity
print(component.render_js())
```

If you only want to pre-compile a JSX file to JS, you can bundle your component into a single file by 
calling `bundle_component`.

```python
from react.bundle import bundle_component

bundle = bundle_component(
    # A path to a file exporting your React component
    'path/to/component.jsx,
    # Translate the source to JavaScript from JSX + ES6/7
    translate=True
)

# Renders a script element pointing to the bundled component
print(bundle.render())

# Outputs the variable name that the component is exposed as.
print(bundle.get_var())
```


Documentation
-------------

- [Installation](#installation)
- [render_component()](#render_component)
- [RenderedComponent](#renderedcomponent)
- [bundle_component()](#bundle_component)
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


render_component()
------------------

Renders a component to its initial HTML. You can use this method to generate HTML
on the server and send the markup down on the initial request for faster page loads
and to allow search engines to crawl your pages for SEO purposes.

Returns a `RenderedComponent` instance, which can be passed directly into templates 
to output the component's HTML, and to mount the component for client-side interactivity.


### Usage

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
    # An optional boolean indicating that the component should be translated
    # from JSX and ES6/7 before rendering. Components are translated with Babel
    translate = True,
    # An optional boolean indicating that the component should be bundled for
    # reuse on the client-side. If `translate` is set to True, this argument is ignored
    bundle = True,
    # An optional boolean indicating that React's `renderToStaticMarkup`
    # method should be used, rather than `renderToString`
    to_static_markup = False,
    # An optional class which is used to encode the props to JSON
    json_encoder=None,
)
```


RenderedComponent
-----------------

The result of rendering a component to its initial markup. RenderedComponents can be 
converted to strings to output their generated markup. If `translate` or `bundle` was
provided to `render_component`, they can also be mounted on the client-side to provide
immediate interactivity.

```python
component = render_component(...)

# Outputs the generated markup
str(component)

# Also outputs the generated markup
component.render_markup()

# Render JS which will remount the component over the call
component.render_js()
```

Note: if you wish to use the `render_js` method on the client-side, you **must** provide a 
`<script>` element pointing to React. React is omitted from the bundled component so that 
build times are reduced, and to ensure that multiple components can be included on a single 
page without duplicating React's codebase.

Be aware that the mounting strategy used by `render_js` is only intended for convenience. If you 
want to use a more custom solution for mounting or bundling, there are a couple of helpers provided 
to assist:

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


bundle_component()
------------------

Packages a React component so that it can be re-used on the client-side. JSX + ES6+7 files are translated
to JavaScript with [Babel](https://babeljs.io/).

Be aware that `bundle_component` is primarily a convenience method. It plugs a pre-built webpack config 
into [python-webpack](https://github.com/markfinger/python-webpack).

If you require more flexibility in the bundling process, you are recommended to read the code to understand
what is happening, and then use python-webpack yourself.


### Usage

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


Running the tests
-----------------

```bash
mkvirtualenv django-react
pip install -r requirements.txt
python runtests.py
```
