Django React
============

Render and bundle React components from a Django application.

Documentation
-------------

- [Basic usage](#basic-usage)
- [Installation](#installation)
- [Running the tests](#running-the-tests)

Basic usage
-----------

Define your component

```python
from django_react import ReactComponent

class MyComponent(ReactComponent):
    source = 'path/to/file.jsx'
```

Create an instance of your component and pass it some props

```python
my_component = MyComponent(
    some_prop='foo',
    some_other_prop=[1, 2, 3]
)
```

In your template you can now render the component to a string and
inject your component's JavaScript.

```html
{{ my_component.render_to_string }}

<script src="path/to/react.js"></script>

{{ my_component.render_js }}
```

The rendered JavaScript will automatically include:
- Your props, serialised to JSON
- Your source, which will have been JSX transformed and bundled with Webpack
- Initialization code that immediately mounts your component with React

The user will see the rendered component immediately and React will automatically
start to add interactivity as the page loads the JavaScript.

Installation
------------

```bash
pip install django-react
```

Add `'django_react'` to your INSTALLED_APPS setting
```python
INSTALLED_APPS = (
    # ...
    'django_react',
)
```

Dependencies
------------

TODO

ReactComponent
--------------

TODO

ReactBundle
-----------

A `django_webpack.WebpackBundle` which is configured to:
- support loading JSX files
- omit React from the generated bundle

You can extend the Webpack configuration by inheriting from ReactBundle
and assigning the class as a `bundle` attribute on your component class.

```python
from django_react import ReactBundle, ReactComponent

class JqueryOptimisedReactBundle(ReactBundle):
    no_parse = ('jquery',)

class MyComponent(ReactComponent):
    bundle = JqueryOptimisedReactBundle
```

react.render()
--------------

A method which allows you to directly render a component with props.

Arguments:

- `path_to_source`: an absolute path to a JS or JSX file which exports the component.
- `serialized_props`: [optional] a string containing the JSON serialised props which will
  be passed to the component
- `to_static_markup`: [optional] a boolean indicating that React's `render_to_static_markup`
  method should be used for the rendering. Use this if you only wish to render the component to HTML and
  React will not be used on the client side.

```python
import json
from django_react import react

props = {
    'some_prop': 1,
    'some_other_prop': [1, 2, 3],
}

rendered_component = react.render(
    path_to_entry='/path/to/component.jsx',
    serialised_props=json.dumps(props),
)
```

Running the tests
-----------------

```bash
mkvirtualenv django-react
pip install -r requirements.txt
python django_react/tests/runner.py
```
