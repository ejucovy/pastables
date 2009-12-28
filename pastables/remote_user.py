def filter_factory(global_conf, user_whitelist=None, user_blacklist=None):
    if user_whitelist:
        user_whitelist = user_whitelist.split()
    if user_blacklist:
        user_blacklist = user_blacklist.split()

    def filter(app):
        return Filter(
            app,
            user_whitelist=user_whitelist, user_blacklist=user_blacklist)
    return filter

from webob import Request
from webob import exc

class RequireRemoteAuth(object):

    whitelist = []
    blacklist = []
    
    def __init__(self, whitelist, blacklist):
        self.whitelist = whitelist or self.whitelist
        self.blacklist = blacklist or self.blacklist

    def match(self, req):
        user = req.remote_user
        if not user:
            return False

        if self.whitelist and user not in self.whitelist:
            return False

        if self.blacklist and user in self.blacklist:
            return False

        return True

class Filter(object):

    def __init__(self, app, whitelist, blacklist):
        self.app = app
        self.filter = RequireRemoteAuth(whitelist, blacklist)

    # XXX TODO: overridable somehow with config
    @property
    def default_app(self):
        return exc.HTTPUnauthorized()

    def __call__(self, environ, start_response):
        req = Request(environ)

        if self.filter.match(req):
            return self.app(environ, start_response)
        return self.default_app(environ, start_response)
