Django + React + Webpack demo
=============================

This demo illustrates how:
- A single codebase can be used to generate server-side 
rendered HTML as well client-side interactivity.
- To pre-render HTML so that you can optimise for search-engines.
- Server-side rendering enables you to gracefully-degrade 
interactive features on clients without JavaScript enabled.


Install
-------

```bash
# In the /example directory

mkvirtualenv django-react-demo
pip install -r requirements.txt

# Start the node server that we use to render and bundle components
./manage.py start_node_server

# In another terminal, start the django devserver
./manage.py runserver
```

And visit http://127.0.0.1:8000

**Note** that the first request may take a while to render, this is down to the 
node server having to read the app's codebase into memory and process dependencies.
The initial overhead will only occurr on the first request, successive requests will 
be rendered immediately.

If you make changes to the app's JS codebase, the node server will detect the changes
and perform incremental rebuilds so that when the next request comes in, everything
is ready and immediately responsive.
