Django + React demo
===================


Install
-------

```bash
# In the /example directory

mkvirtualenv django-react-demo
pip install -r requirements.txt
./manage.py install_package_dependencies
./manage.py runserver
```

And visit http://127.0.0.1:8000

**Note** that the first request may take a while to render, this is down to the 
server having to read the app's codebase into memory and process dependencies.
The initial overhead is unfortunate, but will only occurr the first time that
the node server loads the codebase, successive requests will be rendered immediately.
