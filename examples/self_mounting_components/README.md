Running the example
===================

Install the dependencies

```
pip install -r requirements.txt
npm install
```

Start the webpack-build server

```
npm run webpack-build
```

Start the python server

```
python example.py
```

And visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

----------------------

With `DEBUG = True`, the render server is unneeded. In production you would also want to start
the render server.

```
node server.js
````