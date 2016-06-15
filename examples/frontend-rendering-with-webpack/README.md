Running the example
===================

As mentioned in the ***Using React on the front-end*** section, [Webpack](https://webpack.github.io/) is used to bundle the respective js files into `dist.js` and included in `index.html`. To make React attributes like `onClick` etc. work, the app has to be re-rendered (along with all the props passed down) when it loads on the browswer. React is intelligent enough to not re-paint the browser and only update the changes, thus adding all the component properties.

In this example, the basic_rendering example is modified to submit the Comment Form through ajax and update the Comment List by fetching the updated comments and rendering the application with new props.

### Usage
Install the dependencies

```
pip install -r requirements.txt
npm install
```
### Usage in development
Extending the explanation in the [README](https://github.com/markfinger/python-react/blob/master/README.md#usage-in-development) section of the repo, restarting the render server everytime a change is made in the `.jsx` files can be avoided, by running:
```
npm run watch
```
alongside the python dev server:
```
python example.py
```
The forever utility check for changes and restarts the `render_server` accordingly. 

### Usage in production
Node server can be hosted in multiple ways. Either in the same box as flask server, or elsewhere. One way is to run it as a supervisord job on the same server. The React app needs to bundled as production ready before deploying the python server. This bundle is included in the `base` template for the app to render again on the client side. For bundling, run:
```
npm run postinstall
```
