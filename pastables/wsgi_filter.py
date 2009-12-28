from webob import Request
from webob import exc

class Filter(object):    
    def __init__(self, app, filter_factory, **kw):
        self.app = app
        self.filter = filter_factory(**kw)

    # XXX TODO: overridable somehow with config
    @property
    def default_app(self):
        return exc.HTTPNotFound()

    def __call__(self, environ, start_response):
        req = Request(environ)

        if self.filter.match(req):
            return self.app(environ, start_response)
        return self.default_app(environ, start_response)
