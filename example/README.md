python + react example
======================

This example illustrates how:
- A single codebase can be used to generate server-side 
  rendered HTML as well client-side interactivity.
- To pre-render HTML so that you can optimise for search-engines.
- Server-side rendering enables you to gracefully-degrade 
  interactive features on clients without JavaScript enabled.


Running the example
-------------------

```bash
pip install -r requirements.txt
npm install
python example.py
```

And visit [http://127.0.0.1:8000](http://127.0.0.1:8000)

**Note** that the first request may take a while to render, this is down to the 
node server having to read the app's codebase into memory. The initial overhead
will only occur on the first request, subsequent requests will be rendered
immediately.

If you make changes to the app's JS codebase, the node server will detect the
changes and perform incremental rebuilds so that when the next request comes in,
everything is ready and immediately responsive.
