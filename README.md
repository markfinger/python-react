Django React
============

[![Build Status](https://travis-ci.org/markfinger/django-react.svg?branch=master)](https://travis-ci.org/markfinger/django-react)

Render and bundle React components from a Django application.

```python
from django_react.render import render_component

# Render a JSX component
component = render_component('path/to/component.jsx', translate=True, props={
	'foo': 'bar',
    'woz': [1,2,3],
})

# The rendered markup
print(component)

# Render JavaScript that will reuse the data provided and mount the component
# on the client-side
print(component.render_js())
```

Documentation
-------------

- [Installation](#installation)
- [render_component()](#render_component)
- [RenderedComponent](#renderedcomponent)
- [Running the tests](#running-the-tests)

Installation
------------

```bash
pip install django-react
```

Add django-node and django-react to your `INSTALLED_APPS` setting

```python
INSTALLED_APPS = (
    # ...
    'django_node',
    'django_react',
)
```

Configure django-node to host django-react's renderer.

```python
DJANGO_NODE = {
    'SERVICES': (
        'django_react.services',
    ),
}
```

Start the node server which hosts the renderer.

```bash
./manage.py start_node_server
```

**Note**: you *can* omit the step of starting the server manually, 
as the python process will start it as a subprocess if it is not 
already running. In general though, you are strongly recommended 
to run it as an external process as the performance will be greatly
improved.


render_component()
------------------

Renders a component to its initial HTML. You can use this method to generate HTML
on the server and send the markup down on the initial request for faster page loads
and to allow search engines to crawl your pages for SEO purposes.

Returns a `RenderedComponent` instance, which can be passed directly into templates 
to output the component's HTML.

**Note**: components are loaded with [Babel](http://babeljs.io) which enables you 
to use JSX + ES6/7 in your components.

Arguments:

- `path_to_source` — a path to a JS or JSX file which exports the component. If the 
  path is relative, django's static file finders will be used to find the file.
- `props` *optional* — a dictonary that will be serialised to JSON and passed to 
  the component during the renderering process.
- `to_static_markup` *optional* — a boolean indicating that React's `renderToStaticMarkup`
  method should be used for the rendering. Defaults to `False`, which causes React's 
  `renderToString` method to be used.
- `bundle` *optional* - a boolean indicating that the component should be bundled for
  reuse on the client-side. If `translate` or `watch_source` are used, this argument is
  ignored.
- `translate` *optional* - a boolean indicating that the component should be translated
  from JSX and ES6/7 before rendering.
- `watch_source` *optional* — a boolean indicating that the renderer should watch your source
  files and rebuild the component whenever it changes. If not defined, defaults to `DEBUG`.
- `json_encoder` *optional* — a class which is used to encode the props to JSON. Defaults
  to `django.core.serializers.json.DjangoJSONEncoder`.


RenderedComponent
-----------------

The result of rendering a component to its initial markup. RenderedComponents can be passed
directly into templates where they will output the generated markup.

```python
# Render the component
component = render_component(...)

# Print the generated markup
print(component)
```
```html
<!-- Insert the generated HTML into your template -->
{{ component }}
```

Components can be remounted on the client-side, so that the same codebase and data
can be reused to provide interactivity.

```html
<script src="path/to/react.js"></script>

{{ component.render_js }}
```

*Note*: if you wish to use the `render_js` method, you *must* provide a `<script>` element
pointing to React. React is omitted from the bundled component so that build times are reduced,
and to ensure that multiple components can be included on a single page without duplicating
React's codebase.

Be aware that the mounting strategy used by `render_js` is fairly basic, if you want to use
a more custom solution there are a couple of helpers provided to assist:
```python
The data used to render the component, this can be plugged straight into the client-side
print(component.render_props())

# The bundled component (a WebpackBundle instance)
component.get_bundle()

# Render a script element pointing to the bundled component
print(component.get_bundle().render())

# The variable that the bundle exposes the component as on the global scope
print(component.get_var())

# Returns an absolute path to the location of the component's bundle on the file-system
print(component.bundle.get_path())

# When rendering a bundled component, the component is wrapped in a container
# element to allow the mount JS to target it. You can use this selector to
# target the container element
print(component.get_container_id())

# The rendered markup without the container element wrapping it
print(component.markup)

# Render the JS used to mount the bundled component over the rendered component
print(component.render_mount_js())
```


Running the tests
-----------------

```bash
mkvirtualenv django-react
pip install -r requirements.txt
python runtests.py
```
