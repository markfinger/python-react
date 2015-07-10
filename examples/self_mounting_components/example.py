import os
import json
from flask import Flask, render_template, request, redirect, jsonify
from react.conf import settings as react_settings
from react.render import render_component
from webpack.conf import settings as webpack_settings
from webpack.compiler import webpack

DEBUG = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# As a convenience for development, only connect to the
# render server when DEBUG is False
react_settings.configure(RENDER=not DEBUG)

webpack_settings.configure(
    STATIC_ROOT=os.path.join(BASE_DIR, 'static'),
    STATIC_URL='/static/',
    WATCH=DEBUG,
    HMR=DEBUG,
    CONFIG_DIRS=BASE_DIR,
    CONTEXT={
        'DEBUG': DEBUG,
    },
)


app = Flask(__name__)
app.debug = DEBUG

comments = []


@app.route('/')
def index():
    config_file = os.path.join(BASE_DIR, 'example.webpack.js')

    component = os.path.join(BASE_DIR, 'app', 'CommentBox.jsx')

    props = {
        'comments': comments,
        'url': '/comment/',
    }

    rendered = render_component(component, props)

    webpack_context = {
        'component': component,
        'props_var': 'window.mountProps',
        'container': 'mount-container',
    }

    bundle = webpack(config_file, context=webpack_context)

    return render_template(
        'index.html',
        bundle=bundle,
        webpack_context=webpack_context,
        rendered=rendered,
    )


@app.route('/comment/', methods=('POST',))
def comment():
    comments.append({
        'name': request.form['name'],
        'text': request.form['text'],
    })

    if request.is_xhr:
        return jsonify(comments=comments)

    return redirect('/')



if __name__ == '__main__':
    app.run()