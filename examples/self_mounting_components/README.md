python + react - self mounting components
=========================================

This example illustrates a workflow where webpack is used to generate bundles so that the root React
component can immediately mount itself over the markup that was pre-rendered with the same data.

This workflow is similar to what was provided in older versions of python-react. It can be useful
if you want to add a little interactivity to an otherwise backend-heavy site.

Be aware that while this workflow can be initially convenient, it tends to rely on components maintaining
large amounts of state. A better workflow is for your components to minimize state by delegating all
data storage to external services. If you're looking for something to handle your data, the multitude
of Flux implementations are a reasonable starting point.


### Running the example

Install the dependencies

```
pip install -r requirements.txt
npm install
```

Start the server

```
node server.js
```

Start the python server

```
python example.py
```

And visit [http://127.0.0.1:5000](http://127.0.0.1:5000)