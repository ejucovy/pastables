from webob.exc import *

def composite_factory(loader, global_conf, **local_conf):
    get = loader.get_app(local_conf['get'])
    post = loader.get_app(local_conf['post'])
    return MethodDispatcher(get, post)
    
class MethodDispatcher(object):
    def __init__(self, get, post):
        self.get = get
        self.post = post

    def __call__(self, environ, start_response):
        method = environ['REQUEST_METHOD']
        if method == "GET":
            return self.get(environ, start_response)
        if method == "POST":
            return self.post(environ, start_response)

        return HTTPMethodNotAllowed()(environ, start_response)
