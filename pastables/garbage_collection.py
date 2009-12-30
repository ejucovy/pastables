import gc

class GarbageCollectingMiddleware(object):
    def __init__(self, app, log_environ_key=None):
        self.app = app
        self.log_key = log_environ_key

    def __call__(self, environ, start_response):
        res = self.app(environ, start_response)

        n = gc.collect()
        if n and self.log_key and self.log_key in environ:
            environ[self.log_key].debug(
                self,
                'Garbage-collected %s unreachable objects' % n)
        return res

def filter_factory(global_conf):
    def filter(app):
        return GarbageCollectingMiddleware(app)
    return filter
