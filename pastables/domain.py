from webob.exc import *

def composite_factory(loader, global_conf, **local_conf):
    return MethodDispatcher()
    
class MethodDispatcher(object):
    def __call__(self, environ, start_response):
        import pdb; pdb.set_trace()
        method = environ['REQUEST_METHOD']
        if method == "GET":
            return self.get(environ, start_response)
        if method == "POST":
            return self.post(environ, start_response)

        return HTTPMethodNotAllowed()(environ, start_response)
