import json
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django_react.render import render_component

# An in-memory store of comment objects
comments = []


def index(request):
    # Param flag to deactivate client-side Javascript
    no_js = 'no-js' in request.GET

    # Render the CommentBox component down to HTML
    comment_box = render_component(
        # The path to the component is resolved via Django's static-file
        # finders
        'components/CommentBox.jsx',

        # We can pass data along to the component which will be
        # accessible from the component via its `this.props` property
        props={
            'comments': comments,
            'url': reverse('comment'),
            'pollInterval': 2000,
        },

        # Ensure that the source code is translated to JS from JSX & ES6/7.
        # This enables us to use future-facing JS in across the client-side
        # and server-side
        translate=True,

        # If we intend to use React on the client-side, React will
        # add extra attributes to the HTML so that the initial mount
        # is faster, however these extra attributes are unnecessary
        # if there is no JS on the client-side
        to_static_markup=no_js
    )

    return render(request, 'index.html', {
        'comment_box': comment_box,
        'no_js': no_js,
    })


def comment(request):
    if request.POST:
        comments.append({
            'author': request.POST.get('author', None),
            'text': request.POST.get('text', None),
        })
        if not request.is_ajax():
            return redirect('index-no-js')
    return HttpResponse(
        json.dumps(comments),
        content_type='application/json'
    )