django-react example
====================

This example illustrates how:
- A single codebase can be used to generate server-side 
  rendered HTML as well client-side interactivity.
- To pre-render HTML so that you can optimise for search-engines.
- Server-side rendering enables you to gracefully-degrade 
  interactive features on clients without JavaScript enabled.


Run the example
---------------

```bash
# In the /example directory

# Create a virtual environment for the example
mkvirtualenv django-react-example

# Install the project's python dependencies
pip install -r requirements.txt

# Install the project's JS dependencies
./manage.py install_package_dependencies

# Start the node server that we use to render and bundle components
./manage.py start_node_server

# In another shell, start the django devserver
./manage.py runserver
```

And visit [http://127.0.0.1:8000](http://127.0.0.1:8000)

**Note** that the first request may take a while to render, this is down to the 
node server having to read the app's codebase into memory. The initial overhead
will only occur on the first request, subsequent requests will be rendered
immediately.

If you make changes to the app's JS codebase, the node server will detect the
changes and perform incremental rebuilds so that when the next request comes in,
everything is ready and immediately responsive.
