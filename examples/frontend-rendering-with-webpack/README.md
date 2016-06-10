Running the example
===================

As mentioned in the ***Using React on the front-end*** section, [Webpack](https://webpack.github.io/) is used to bundle the respective js files into `dist.js` and included in `index.html`. To make React attributes like `onClick` etc. work, the app has to be re-rendered (along with all the props passed down) when it loads on the browswer. React is intelligent enough to not re-paint the browser and only update the changes, thus adding all the component properties.

Install the dependencies

```
pip install -r requirements.txt
npm install
```

Start the render server

```
node render_server.js
```

Start the python server

```
python example.py
```

And visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Notes



