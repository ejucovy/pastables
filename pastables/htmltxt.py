from webob import Request

class PreTextFilter(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        req = Request(environ)
        res = req.get_response(self.app)
        if res.status_int == 200 and res.content_type == 'text/plain':
            res.content_type = 'text/html'
            res.body = "<pre>%s</pre>" % res.body
        return res(environ, start_response)

def filter_factory(global_conf, **kw):
    def filter(app):
        return PreTextFilter(app)
    return filter
