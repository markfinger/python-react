import os
from flask import Flask, render_template, request, redirect
from react.render import render_component

DEBUG = True

app = Flask(__name__)
app.debug = DEBUG

comments = []

@app.route('/')
def index():
    rendered = render_component(
        os.path.join(os.getcwd(), 'static', 'js', 'CommentBox.jsx'),
        {
            'comments': comments,
            'url': '/comment/',
        },
        to_static_markup=True,
    )

    return render_template('index.html', rendered=rendered)


@app.route('/comment/', methods=('POST',))
def comment():
    comments.append({
        'author': request.form['author'],
        'text': request.form['text'],
    })
    return redirect('/')


if __name__ == '__main__':
    app.run()