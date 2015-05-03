import os
from flask import Flask, render_template, request, redirect, jsonify
from react.render import render_component
from settings import DEBUG, BASE_DIR

app = Flask(__name__)
app.debug = DEBUG

comments = []


@app.route('/')
def index():
    no_js = 'no-js' in request.args

    comment_box = render_component(
        # An absolute path to the component
        os.path.join(BASE_DIR, 'static', 'jsx', 'CommentBox.jsx'),

        # The data that we use to render the component and mount it
        # on the client-side
        props={
            'comments': comments,
            'url': '/comment/',
            'pollInterval': 2000,
        },

        # Ensure that the source code is translated to JS from JSX & ES6/7.
        # This enables us to use future-facing JS across the client-side
        # and server-side
        translate=True,

        # If you do not intend to use React on the client-side, rendering
        # to static markup will optimise the generated markup
        to_static_markup=no_js
    )

    return render_template('index.html', comment_box=comment_box, no_js=no_js)


@app.route('/comment/', methods=('GET', 'POST'))
def comment():
    if request.method == 'POST':
        comments.append({
            'author': request.form['author'],
            'text': request.form['text'],
        })

        if not request.is_xhr:
            return redirect('/?no-js')

    return jsonify(comments=comments)


if __name__ == '__main__':
    app.run()