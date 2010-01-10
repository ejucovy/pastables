from webob import Request, Response

class ImgLinkFilter(object):
    def __init__(self, app, raw_link):
        self.app = app
        self.raw_link = raw_link

    def __call__(self, environ, start_response):
        location = environ['PATH_INFO']
        raw_link = self.raw_link % location
        req = Request(environ)
        res = req.get_response(self.app)

        if req.path_qs == raw_link:
            return res(environ, start_response)
        if environ.get('HTTP_ACCEPT', '').startswith('image/'):
            return res(environ, start_response)

        if res.content_type.startswith('image/'):
            return Response("""<a href="%s"><img src="%s" /></a>""" % (raw_link, raw_link)
                            )(environ, start_response)

        return res(environ, start_response)

def filter_factory(global_conf, raw_link=None, **kw):
    def filter(app):
        return ImgLinkFilter(app, raw_link)
    return filter
