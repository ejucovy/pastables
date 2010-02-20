def filter_factory(global_conf, match=None, replace_with=None, **app_conf):
    def filter(app):
        return Rewrite(app, match, replace_with)
    return filter

from webob import Request

class Rewrite(object):

    def __init__(self, app, match, replace_with):
        self.app = app
        self.match = match
        self.replace_with = replace_with

    def __call__(self, environ, start_response):
        req = Request(environ)

        res = req.get_response(self.app)

        if res.location is not None and res.location.startswith(self.match):
            res.location = "%s%s" % (self.replace_with, res.location[len(self.match):])

        return res(environ, start_response)
