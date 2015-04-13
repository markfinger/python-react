django-react
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
- [Usage in development](#usage-in-development)
- [Usage in production](#usage-in-production)
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
    'django_webpack',
    'django_react',
)
```

Ensure that Django can find the bundles generated from your components

```
STATICFILES_FINDERS = (
    # ...
    'django_webpack.staticfiles.WebpackFinder',
)
```

Configure django-node to host django-webpack and django-react.

```python
DJANGO_NODE = {
    'SERVICES': (
        'django_webpack.services',
        'django_react.services',
    ),
}
```


render_component()
------------------

Renders a component to its initial HTML. You can use this method to generate HTML
on the server and send the markup down on the initial request for faster page loads
and to allow search engines to crawl your pages for SEO purposes.

Returns a `RenderedComponent` instance, which can be passed directly into templates 
to output the component's HTML.

Arguments:

- **path_to_source** — a path to a JS or JSX file which exports the component. If the 
  path is relative, django's static file finders will be used to find the file.
- **props** *optional* — a dictonary that will be serialised to JSON and passed to 
  the component during the renderering process.
- **to_static_markup** *optional* — a boolean indicating that React's `renderToStaticMarkup`
  method should be used for the rendering. Defaults to `False`, which causes React's 
  `renderToString` method to be used.
- **bundle** *optional* - a boolean indicating that the component should be bundled for
  reuse on the client-side. If `translate` or `watch_source` are used, this argument is
  ignored.
- **translate** *optional* - a boolean indicating that the component should be translated
  from JSX and ES6/7 before rendering. Components are translated with
  [Babel](http://babeljs.io).
- **watch_source** *optional* — a boolean indicating that the renderer should watch your source
  files and rebuild the component whenever it changes. If not defined, defaults to `DEBUG`.
- **json_encoder** *optional* — a class which is used to encode the props to JSON. Defaults
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

**Note**: if you wish to use the `render_js` method, you **must** provide a `<script>` element
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

Usage in development
--------------------

When running in development, you are **strongly** recommended to run the
node server as an external process. By using a separate process, the 
node server will be able to persist in-memory caches of your source files.

The server can be started by running the `start_node_server` management
command, for example:

```bash
# Run the node server as an external process. You will need
# to run your python process in another shell
./manage.py start_node_server
```

If you use the default behaviour - and do not start the server yourself - 
the node server will be run as a detached process that will be restarted 
whenever the python process restarts. Given how easy it is to trigger a 
restart of a django devserver, this means that your node server will 
frequently have to restart and rebuild your source files.


Usage in production
-------------------

When running in production, you are **strongly** recommended to use a 
process supervisor, such as [supervisor](http://supervisord.org/) or
[PM2](https://github.com/Unitech/pm2) to control the node server that
django-react and django-webpack use.

The server can be started by running the `start_node_server` management
command, for example:

```bash
./manage.py start_node_server
```

You can configure your supervisor process to use your virtual environment's
python to target the manage.py file and run the `start_node_server` 
management command.


Running the tests
-----------------

```bash
mkvirtualenv django-react
pip install -r requirements.txt
python runtests.py
```
