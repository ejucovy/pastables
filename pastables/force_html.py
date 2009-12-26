def filter_factory(content_type=None, *args):
    def filter(app):
        return ForceHtml(app, content_type=content_type)
    return filter

from webob import Request

class ForceHtml(object):

    content_type = 'text/html'

    def __init__(self, app, content_type=None):
        self.app = app
        self.content_type = content_type or self.content_type

    def __call__(self, environ, start_response):
        req = Request(environ)

        res = self.app(environ, start_response)
        res.content_type = self.content_type

        return res(environ, start_response)
