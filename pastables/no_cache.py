from webob import Request
from webob import exc

def filter_factory(*args, **kw):
    return Filter

class Filter(object):

    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        req = Request(environ)
        req.remove_conditional_headers()
        res = req.get_response(self.app)
        return res(environ, start_response)
        
