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

The user will see the rendered component immediately and, once the
page has loaded the JavaScript, React will automatically start to add
interactivity.

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

Running the tests
-----------------

```bash
mkvirtualenv django-react
pip install -r requirements.txt
python django_react/tests/runner.py
```
