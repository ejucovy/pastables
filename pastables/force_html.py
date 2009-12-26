def filter_factory(*args):
    def filter(app):
        return ForceHtml(app)
    return filter

from webob import Request

class ForceHtml(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        req = Request(environ)
        res = req.get_response(self.app)
        res.content_type = 'text/html'
        return res(environ, start_response)
