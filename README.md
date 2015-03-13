Django React
============

[![Build Status](https://travis-ci.org/markfinger/django-react.svg?branch=master)](https://travis-ci.org/markfinger/django-react)

Render React components from a Django application.

```python
from django_react.render import render_component

props = {
    'foo: 'bar',
    'woz': [1,2,3],
}

rendered = render_component('path/to/component.jsx', props=props)

print(rendered)
```

Documentation
-------------

- [Installation](#installation)
- [render_component()](#render_component)
- [RenderedComponent](#renderedcomponent)
- [Running the tests](#running-the-tests)

Installation
------------

**Note**: django-react is currently under active development and the latest
stable version from PyPI is functional but far, far slower. In practice, you 
are recommended to use a recent version from master branch. django-react depends 
on django-node, which is in a similar position of active development, so you
will also need to use its master branch as well.

```bash
pip install -e git+https://github.com/markfinger/django-node.git#egg=django-node
pip install -e git+https://github.com/markfinger/django-react.git#egg=django-react
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
)
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

Arguments:

- `path_to_source` - an path to a JS or JSX file which exports the component. If the 
  path is relative, django's static file finders will be used to find the file.
- `props` *optional* - a dictonary that will be serialised to JSON and passed in 
  to the component as props during the renderering process.
- `to_static_markup` *optional* - a boolean indicating that React's `render_to_static_markup`
  method should be used for the rendering. Set this to True if you are rendering the component
  to static HTML and React will not be used on the client-side.
- `watch_source` *optional* - a boolean indicating that the renderer should watch your source
  files and rebuild the component everytime it changes. Defaults to `True`, in development.
- `json_encoder` *optional* - a class which is used to encode the JSON which is sent to the 
  renderer. Defaults to `django.core.serializers.json.DjangoJSONEncoder`.


RenderedComponent
-----------------

The result of rendering a component to its initial HTML. RenderedComponents can be passed
directly into templates where they output the generated HTML.

```python
# Render the component
my_component = render_component(...)

# Print the generated HTML
print(my_component)
```
```html
<!-- Insert the generated HTML into your template -->
{{ my_component }}
```

RenderedComponents have a helper method, `render_props`, which outputs your JSON-serialized 
props. This allows you to reuse the encoded form of your props on the client-side.

```html
<script>
    var myProps = {{ my_component.render_props }};
</script>
```


Running the tests
-----------------

```bash
mkvirtualenv django-react
pip install -r requirements.txt
python runtests.py
```
