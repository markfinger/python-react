import os
import tornado.ioloop
import tornado.httpserver
from tornado.web import RequestHandler
from tornado.gen import coroutine
from react.render import render_component


comments = []

class IndexHandler(RequestHandler):
    @coroutine
    def get(self):
        rendered = render_component(
        os.path.join(os.getcwd(), 'static', 'js', 'CommentBox.jsx'),
        {
            'comments': comments,
            'url': '/comments',
            'xsrf':self.xsrf_token
        },
        to_static_markup=False,
        )
        self.render('index.html', rendered=rendered)


class CommentHandler(RequestHandler):
    @coroutine
    def post(self):
        comments.append({
        'author': self.get_argument('author'),
        'text': self.get_argument('text'),
        })
        self.redirect('/')


urls = [
    (r"/", IndexHandler),
    (r"/comments", CommentHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path":r"{0}".format(os.path.join(os.path.dirname(__file__),"static"))}),
]

settings = dict({
    "template_path": os.path.join(os.path.dirname(__file__),"templates"),
    "static_path": os.path.join(os.path.dirname(__file__),"static"),
    "cookie_secret": os.urandom(12),
    "xsrf_cookies": True,
    "debug": True,
    "compress_response": True
})

application = tornado.web.Application(urls,**settings)


if __name__ == "__main__":
    server = tornado.httpserver.HTTPServer(application)
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

