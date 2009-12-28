def filter_factory(qs_key=None, qs_val=None, remove_key=False, *args):
    def filter(app):
        return RequireQueryString(app, qs_key=qs_key, qs_val=qs_val, remove_key=remove_key)
    return filter

from webob import Request
from webob import exc

class RequireQueryString(object):

    qs_key = None
    qs_val = None

    def __init__(self, app, qs_key=None, qs_val=None, remove_key=False):
        self.app = app
        self.qs_key = qs_key or self.qs_key
        self.qs_key = qs_val or self.qs_val
        self.remove_key = remove_key

    # XXX TODO: overridable somehow with config
    @property
    def default_app(self):
        return exc.HTTPNotFound()

    def __call__(self, environ, start_response):
        req = Request(environ)
        if not self.qs_key:
            return self.app(environ, start_response)

        if self.qs_key not in req.GET:
            return self.default_app(environ, start_response)

        qs_val = req.GET[self.qs_key]
        if self.remove_key:
            del req.GET[self.qs_key]

        if not self.qs_val:
            return self.app(environ, start_response)

        if qs_val != self.qs_val:
            return self.default_app(environ, start_response)

        return self.app(environ, start_response)