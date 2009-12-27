from webob.exc import *

def composite_factory(loader, global_conf, **local_conf):
    apps = {}
    for host, appname in local_conf.items():
        host = host.upper()
        assert host not in apps, "Duplicate assignment for request method %s" % s
        apps[host] = loader.get_app(appname)
    return MethodDispatcher(apps)
    
class MethodDispatcher(object):
    def __init__(self, apps):
        self.methods = dict(apps)

    def __call__(self, environ, start_response):
        method = environ['REQUEST_METHOD']
        if method in self.methods:
            return self.methods[method](environ, start_response)

        return HTTPMethodNotAllowed()(environ, start_response)
