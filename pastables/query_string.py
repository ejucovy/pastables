from paste.deploy.converters import asbool

def filter_factory(global_conf, qs_key=None, qs_val=None, remove_key=False):
    remove_key = asbool(remove_key)
    def filter(app):
        return Filter(
            app,
            qs_key=qs_key, qs_val=qs_val, remove_key=remove_key)
    return filter

from webob import Request
from webob import exc

class Filter(object):
    """ a wsgi interface to RequireQueryString """
    def __init__(self, app, qs_key=None, qs_val=None, remove_key=False):
        self.app = app
        self.filter = RequireQueryString(qs_key, qs_val, remove_key)

    # XXX TODO: overridable somehow with config
    @property
    def default_app(self):
        return exc.HTTPNotFound()

    def __call__(self, environ, start_response):
        req = Request(environ)

        if self.filter.match(req):
            return self.app(environ, start_response)
        return self.default_app(environ, start_response)

class RequireQueryString(object):

    qs_key = None
    qs_val = None

    def __init__(self, qs_key=None, qs_val=None, remove_key=False):
        self.qs_key = qs_key or self.qs_key
        self.qs_key = qs_val or self.qs_val
        self.remove_key = remove_key

    def match(self, req):
        if not self.qs_key:
            return True

        if self.qs_key not in req.GET:
            return False

        qs_val = req.GET[self.qs_key]
        if self.remove_key:
            del req.GET[self.qs_key]

        if not self.qs_val:
            return True
        if qs_val != self.qs_val:
            return False
        return True
