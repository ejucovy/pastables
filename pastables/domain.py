from webob.exc import *

def composite_factory(loader, global_conf, **local_conf):
    apps = {}
    for host, appname in local_conf.items():
        assert host not in apps, "Duplicate assignment for host %s" % s
        apps[host] = loader.get_app(appname)
    return MethodDispatcher(apps)
    
# TODO: default?
class MethodDispatcher(object):
    def __init__(self, apps):
        self.hostmap = dict(apps) # copy

    def __call__(self, environ, start_response):
        host = environ['HTTP_HOST'].split(':')[0]
        if host in self.hostmap:
            return self.hostmap[host](environ, start_response)

        return HTTPNotFound()(environ, start_response)
